<?xml version="1.0" encoding="UTF-8" ?>
<Package name="remote" format_version="5">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="." xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="greet" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="big_cheer" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="check_connection" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="goodbye" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="next_task" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="small_cheer" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="try_again" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="dance_robot" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="dance_disco" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="dance_chicken" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="dance_marcarena" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="raise_hand" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="thinking" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="exciting_fun" xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs />
    <Resources>
        <File name="icon" src="icon.png" />
        <File name="__init__" src="scripts/stk/__init__.py" />
        <File name="events" src="scripts/stk/events.py" />
        <File name="logging" src="scripts/stk/logging.py" />
        <File name="runner" src="scripts/stk/runner.py" />
        <File name="services" src="scripts/stk/services.py" />
        <File name="chicken_dance_3" src="music/chicken_dance_3.mp3" />
        <File name="Disco Medusae" src="music/Disco Medusae.mp3" />
        <File name="macarena" src="music/macarena.mp3" />
        <File name="macarena_2" src="music/macarena_2.mp3" />
        <File name="notification-37858" src="music/notification-37858.mp3" />
        <File name="Robobozo" src="music/Robobozo.mp3" />
    </Resources>
    <Topics />
    <IgnoredPaths>
        <Path src="translations/translation_en_US.ts" />
        <Path src="scripts/remote.py" />
        <Path src=".metadata" />
        <Path src="translations" />
        <Path src="scripts/stk/__pycache__" />
    </IgnoredPaths>
    <Translations auto-fill="en_US">
        <Translation name="translation_en_US" src="translations/translation_en_US.ts" language="en_US" />
        <Translation name="translation_nn_NO" src="translations/translation_nn_NO.ts" language="nn_NO" />
    </Translations>
</Package>
