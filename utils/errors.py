import copy

import discord
from discord.ext import commands


class BlacklistedError(commands.CheckFailure):
    """
    An error that gets raised when a user is blacklisted from using the bot.
    """


class MaintenanceError(commands.CheckFailure):
    """
    An error that gets raised when the bot is in maintenance mode.
    """


class IncompatibleOptionsProvided(commands.UserInputError):
    """
    An error that gets raised when incompatible options are provided.
    """


class DiscordExceptions:
    """
    A big LONG list of all errors I may ever need to raise.
    """

    def __init__(self) -> None:
        """
        Initialize the class and add the errors to a big list.
        """
        self.set_python_errors()
        self.set_base_errors()
        self.set_commands_errors()
        self.set_my_errors()

        self.all_errors = (
            copy.deepcopy(self.python_errors)
            + copy.deepcopy(self.base_errors)
            + copy.deepcopy(self.commands_errors)
            + copy.deepcopy(self.my_errors)
        )

        self.errors = {}

        for i in self.all_errors:
            error_as_string = str(i).removeprefix("<class '").removesuffix("'>")
            error = i

            self.errors[error_as_string] = error

    def set_my_errors(self) -> None:
        """
        Set my custom defined errors.
        """
        self.my_errors = [
            BlacklistedError,
            MaintenanceError,
            IncompatibleOptionsProvided,
        ]

    def set_python_errors(self) -> None:
        """
        Set the core errors from python.
        """
        self.python_errors = [
            OverflowError,
            DeprecationWarning,
            ZeroDivisionError,
            RuntimeWarning,
            UnicodeDecodeError,
            StopAsyncIteration,
            EOFError,
            PendingDeprecationWarning,
            ProcessLookupError,
            ArithmeticError,
            NameError,
            PermissionError,
            Warning,
            BytesWarning,
            InterruptedError,
            ValueError,
            GeneratorExit,
            FileExistsError,
            AssertionError,
            MemoryError,
            UserWarning,
            IndentationError,
            LookupError,
            OSError,
            KeyboardInterrupt,
            ConnectionAbortedError,
            ModuleNotFoundError,
            FloatingPointError,
            UnicodeTranslateError,
            ChildProcessError,
            RecursionError,
            UnicodeEncodeError,
            BlockingIOError,
            NotImplementedError,
            AttributeError,
            TimeoutError,
            BaseException,
            TypeError,
            TabError,
            ReferenceError,
            ResourceWarning,
            RuntimeError,
            FutureWarning,
            ImportWarning,
            ConnectionResetError,
            FileNotFoundError,
            BufferError,
            SyntaxError,
            IsADirectoryError,
            ConnectionRefusedError,
            SystemError,
            SyntaxWarning,
            NotADirectoryError,
            UnicodeError,
            KeyError,
            ConnectionError,
            UnboundLocalError,
            SystemExit,
            IndexError,
            ImportError,
            StopIteration,
            UnicodeWarning,
            Exception,
            BrokenPipeError,
        ]

    def set_base_errors(self) -> None:
        """
        Set the base errors from the discord module.
        """
        self.base_errors = [
            discord.DiscordException,
            discord.ClientException,
            discord.LoginFailure,
            discord.HTTPException,
            discord.RateLimited,
            discord.Forbidden,
            discord.NotFound,
            discord.DiscordServerError,
            discord.InvalidData,
            discord.GatewayNotFound,
            discord.ConnectionClosed,
            discord.PrivilegedIntentsRequired,
            discord.InteractionResponded,
            discord.opus.OpusError,
            discord.opus.OpusNotLoaded,
        ]

    def set_commands_errors(self) -> None:
        """
        Set the errors from discord.ext.commands.
        """
        self.commands_errors = [
            commands.CommandError,
            commands.ConversionError,
            commands.MissingRequiredArgument,
            commands.MissingRequiredAttachment,
            commands.ArgumentParsingError,
            commands.UnexpectedQuoteError,
            commands.InvalidEndOfQuotedStringError,
            commands.ExpectedClosingQuoteError,
            commands.BadArgument,
            commands.BadUnionArgument,
            commands.BadLiteralArgument,
            commands.PrivateMessageOnly,
            commands.NoPrivateMessage,
            commands.CheckFailure,
            commands.CheckAnyFailure,
            commands.CommandNotFound,
            commands.DisabledCommand,
            commands.CommandInvokeError,
            commands.TooManyArguments,
            commands.UserInputError,
            commands.CommandOnCooldown,
            commands.MaxConcurrencyReached,
            commands.NotOwner,
            commands.MessageNotFound,
            commands.MemberNotFound,
            commands.GuildNotFound,
            commands.UserNotFound,
            commands.ChannelNotFound,
            commands.ChannelNotReadable,
            commands.ThreadNotFound,
            commands.BadColorArgument,
            commands.RoleNotFound,
            commands.BadInviteArgument,
            commands.EmojiNotFound,
            commands.PartialEmojiConversionFailure,
            commands.GuildStickerNotFound,
            commands.ScheduledEventNotFound,
            commands.BadBoolArgument,
            commands.RangeError,
            commands.MissingPermissions,
            commands.BotMissingPermissions,
            commands.MissingRole,
            commands.BotMissingRole,
            commands.MissingAnyRole,
            commands.BotMissingAnyRole,
            commands.NSFWChannelRequired,
            commands.FlagError,
            commands.BadFlagArgument,
            commands.MissingFlagArgument,
            commands.TooManyFlags,
            commands.MissingRequiredFlag,
            commands.ExtensionError,
            commands.ExtensionAlreadyLoaded,
            commands.ExtensionNotLoaded,
            commands.NoEntryPointError,
            commands.ExtensionFailed,
            commands.ExtensionNotFound,
            commands.CommandRegistrationError,
            commands.HybridCommandError,
        ]
