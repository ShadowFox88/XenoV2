import copy

from discord.ext import commands


class BlacklistedError(commands.CheckFailure):
    pass


class MaintenanceError(commands.CheckFailure):
    pass


class DiscordExceptions:
    def __init__(self):
        self.set_python_errors()
        self.set_base_errors()
        self.set_commands_errors()

        self.all_errors = (
            copy.deepcopy(self.python_errors)
            + copy.deepcopy(self.base_errors)
            + copy.deepcopy(self.commands_errors)
            + copy.deepcopy(self.my_errors)
        )
        
    def set_my_errors(self):
        self.my_errors = [
            "BlacklistedError",
            "MaintenanceError",
        ]

    def set_python_errors(self):
        self.python_errors = [
            "OverflowError",
            "DeprecationWarning",
            "ZeroDivisionError",
            "RuntimeWarning",
            "UnicodeDecodeError",
            "StopAsyncIteration",
            "EOFError",
            "PendingDeprecationWarning",
            "ProcessLookupError",
            "ArithmeticError",
            "NameError",
            "PermissionError",
            "Warning",
            "BytesWarning",
            "InterruptedError",
            "ValueError",
            "GeneratorExit",
            "FileExistsError",
            "AssertionError",
            "MemoryError",
            "UserWarning",
            "IndentationError",
            "LookupError",
            "OSError",
            "KeyboardInterrupt",
            "ConnectionAbortedError",
            "ModuleNotFoundError",
            "FloatingPointError",
            "UnicodeTranslateError",
            "ChildProcessError",
            "RecursionError",
            "UnicodeEncodeError",
            "BlockingIOError",
            "NotImplementedError",
            "AttributeError",
            "TimeoutError",
            "BaseException",
            "TypeError",
            "TabError",
            "ReferenceError",
            "ResourceWarning",
            "RuntimeError",
            "FutureWarning",
            "ImportWarning",
            "ConnectionResetError",
            "FileNotFoundError",
            "BufferError",
            "SyntaxError",
            "IsADirectoryError",
            "ConnectionRefusedError",
            "SystemError",
            "SyntaxWarning",
            "NotADirectoryError",
            "UnicodeError",
            "KeyError",
            "ConnectionError",
            "UnboundLocalError",
            "SystemExit",
            "IndexError",
            "ImportError",
            "StopIteration",
            "UnicodeWarning",
            "Exception",
            "BrokenPipeError",
        ]

    def set_base_errors(self):
        self.base_errors = [
            "discord.DiscordException",
            "discord.ClientException",
            "discord.LoginFailure",
            "discord.HTTPException",
            "discord.RateLimited",
            "discord.Forbidden",
            "discord.NotFound",
            "discord.DiscordServerError",
            "discord.InvalidData",
            "discord.GatewayNotFound",
            "discord.ConnectionClosed",
            "discord.PrivilegedIntentsRequired",
            "discord.InteractionResponded",
            "discord.opus.OpusError",
            "discord.opus.OpusNotLoaded",
        ]

    def set_commands_errors(self):
        self.commands_errors = [
            "discord.ext.commands.CommandError",
            "discord.ext.commands.ConvertionError",
            "discord.ext.commands.MissingRequiredArgument",
            "discord.ext.commands.MissingRequiredAttachment",
            "discord.ext.commands.ArgumentParsingError",
            "discord.ext.commands.UnexpectedQuoteError",
            "discord.ext.commands.InvalidEndOfQuotedStringError",
            "discord.ext.commands.ExpectedClosingQuoteError",
            "discord.ext.commands.BadArgument",
            "discord.ext.commands.BadUnionArgument",
            "discord.ext.commands.BadLiteralArgument",
            "discord.ext.commands.PrivateMessageOnly",
            "discord.ext.commands.NoPrivateMessage",
            "discord.ext.commands.CheckFailure",
            "discord.ext.commands.CheckAnyFailure",
            "discord.ext.commands.CommandNotFound",
            "discord.ext.commands.DisabledCommand",
            "discord.ext.commands.CommandInvokeError",
            "discord.ext.commands.TooManyArguments",
            "discord.ext.commands.UserInputError",
            "discord.ext.commands.CommandOnCooldown",
            "discord.ext.commands.MaxConcurrencyReached",
            "discord.ext.commands.NotOwner",
            "discord.ext.commands.MessageNotFound",
            "discord.ext.commands.MemberNotFound",
            "discord.ext.commands.GuildNotFound",
            "discord.ext.commands.UserNotFound",
            "discord.ext.commands.ChannelNotFound",
            "discord.ext.commands.ChannelNotReadable",
            "discord.ext.commands.ThreadNotFound",
            "discord.ext.commands.BadColorArgument",
            "discord.ext.commands.RoleNotFound",
            "discord.ext.commands.BadInviteArgument",
            "discord.ext.commands.EmojiNotFound",
            "discord.ext.commands.PartialEmojiConversionFailure",
            "discord.ext.commands.GuildStickerNotFound",
            "discord.ext.commands.ScheduledEventNotFound",
            "discord.ext.commands.BadBoolArgument",
            "discord.ext.commands.RangeError",
            "discord.ext.commands.MissingPermissions",
            "discord.ext.commands.BotMissingPermissions",
            "discord.ext.commands.MissingRole",
            "discord.ext.commands.BotMissingRole",
            "discord.ext.commands.MissingAnyRole",
            "discord.ext.commands.BotMissingAnyRole",
            "discord.ext.commands.NSFWChannelRequired",
            "discord.ext.commands.FlagError",
            "discord.ext.commands.BadFlagArgument",
            "discord.ext.commands.MissingFlagArgument",
            "discord.ext.commands.TooManyFlags",
            "discord.ext.commands.MissingRequiredFlag",
            "discord.ext.commands.ExtensionError",
            "discord.ext.commands.ExtensionAlreadyLoaded",
            "discord.ext.commands.ExtensionNotLoaded",
            "discord.ext.commands.NoEntryPointError",
            "discord.ext.commands.ExtensionFailed",
            "discord.ext.commands.ExtensionNotFound",
            "discord.ext.commands.CommandRegistrationError",
            "discord.ext.commands.HybridCommandError",
        ]
