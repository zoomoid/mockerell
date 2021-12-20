module Main where  -- TODO: Refactor this horrible module

import ClassyPrelude
import Data.Text as T (splitOn, breakOn, head, tail)
import Data.Maybe
import System.Environment
import Control.Applicative
import qualified Telegram.Bot.API as Telegram
import qualified Telegram.Bot.API.InlineMode as Telegram
import qualified Telegram.Bot.API.InlineMode.InputMessageContent as Telegram
import qualified Telegram.Bot.API.InlineMode.InlineQueryResult as Telegram
import Telegram.Bot.Simple
import Telegram.Bot.Simple.Debug
import Telegram.Bot.Simple.UpdateParser
import Telegram.Bot.API.InlineMode
import Control.Monad.Reader
import Text.Mock
import Text.Mock.Help (styleHelp)
import Crypto.Hash
import Inline

import System.IO.Unsafe

-- | Run bot reading token from token file.
main :: IO ()
main = do
    lookupEnv "MOCK_BOT_TOKEN" >>= \case
        Nothing -> putStrLn "Please supply bot token in environment variable $MOCK_BOT_TOKEN."
        Just token -> Telegram.defaultTelegramClientEnv (Telegram.Token $ pack token)
            >>= startBot_ (traceBotDefault bot)

-- | Actions bot can perform.
data Action
  = NoAction  -- ^ Perform no action.
  | Reply Text  -- ^ Reply some text.
  | InlineReply [(Text, Text, Text)]
  | SendHelp  -- ^Send help text.
  deriving (Show)

-- | Bot application.
bot :: BotApp () Action
bot = BotApp
    { botInitialModel = ()
    , botAction = \update () -> handleUpdate update
    , botHandler = handleAction
    , botJobs = []
    }

-- | Whether the message was sent in a private chat.
isPrivate :: Telegram.Message -> Bool
isPrivate msg = case Telegram.chatType $ Telegram.messageChat msg of
    Telegram.ChatTypePrivate -> True
    _ -> False

directMock :: UpdateParser Text
directMock = UpdateParser f where
    f :: Telegram.Update -> Maybe Text
    f update = do
        message <- Telegram.updateMessage update
        (command':body') <- words <$> Telegram.messageText message
        let styleNames = splitOn "|" . toLower $ fst $ breakOn "@" $ if T.head command' == '/' then T.tail command' else command'
        let body = unwords body'
        if length styleNames > 5 then
            return "Only concatenations of up to 5 styles are allowed."
        else case concatMaybeFunctions . map (`lookup` styles) $ styleNames of
            Just f -> if body == ""
                then do
                    replyToMessage <- Telegram.messageReplyToMessage message
                    replyToText <- Telegram.messageText replyToMessage
                    return $ f replyToText
                else return $ f body
            _ -> if isPrivate message then return "Invalid mocking. See /help." else fail "Invalid mocking."

replyToInline :: UpdateParser [(Text, Text, Text)]
replyToInline = UpdateParser f where
    f :: Telegram.Update -> Maybe [(Text, Text, Text)]
    f update = do
        inlineQuery <- Telegram.updateInlineQuery update
        let txt = Telegram.inlineQueryQuery inlineQuery
        --let id = Telegram.inlineQueryId inlineQuery
        if txt == ""
            then return []
            else return $ map (\(name, f) -> (
                name,
                f txt,
                pack $ show (Crypto.Hash.hash $ encodeUtf8 (name <> txt) :: Digest SHA256)
                )) styles

-- |Concatenates a list of Maybe functions. Execution goes from left to right.
-- Returns Nothing if any of the elements of the list is Nothing.
concatMaybeFunctions :: [Maybe (a -> a)] -> Maybe (a -> a)
concatMaybeFunctions [] = Just id
concatMaybeFunctions (mf:mfs) = do
    f <- mf
    cf <- concatMaybeFunctions mfs
    return $ cf . f

-- | How to process incoming 'Telegram.Update's
-- and turn them into 'Action's.
handleUpdate :: Telegram.Update -> Maybe Action
handleUpdate = parseUpdate
    $   SendHelp <$ command "help"
    <|> SendHelp <$ command "start"
    <|> Reply <$> directMock
    <|> InlineReply <$> replyToInline

    -- <|> SendHelp <$ text

-- | How to handle 'Action's.
handleAction :: Action -> () -> Eff Action ()
handleAction action model = case action of
    NoAction -> pure model
    (Reply message) -> model <# do
        replyText message
        pure NoAction
    (InlineReply msgs) -> model <# do
        let results = map (\(title, message, id) -> Telegram.InlineQueryResult Telegram.InlineQueryResultArticle (Telegram.InlineQueryResultId id) (Just title) (Just $ Telegram.InputTextMessageContent message Nothing (Just False))) msgs
        Inline.answerInlineQuery results
        pure NoAction
    SendHelp -> model <# do
        reply $ (toReplyMessage help) {replyMessageParseMode = Just Telegram.Markdown, replyMessageDisableWebPagePreview = Just True}
        pure NoAction

-- | Help text.
help :: Text
help = unlines [
    "*Mock " <> version <> "*",
    "A Great BoT tO TRANsFoRM TEXt, wRiTten iN HaSKeLL.",
    "By Nicolas Lenz. [Free and open source under the WTFPL.](https://git.eisfunke.com/software/mock-bot-telegram)",
    "",
    "*Inline usage:* Just type `@truemockbot` and the text you want to stylize in any chat. Telegram will show you a selection of the styles available.",
    "",
    "*Usage:* \\[STYLE] \\[TEXT]",
    "*Example:* `random Cool Text`",
    "",
    "Multiple styles can be concatenated with \'|\'s.",
    "*Example:* `random|double Cool Text`",
    "",
    "*Available Styles:*",
    intercalate "\n" styleHelps] where
        styleHelps = map
            (\(name, _) -> concat ["  *", name, "*: ", styleHelp name])
            styles
