#!/bin/bash
. ./scripts_config.sh

DIR_SATIC_APP='./'

ACTION_EXIT='0'

ACTION_INSTALL_NEED_FOR_GULP='1'
ACTION_NPM_START='2'

ACTION_CLEAN_GLOBAL_STATIC_DIR='3'

ACTION_CLEAN_GLOBAL_STATIC_DIR_DEV_BUILD='4'
ACTION_CLEAN_GLOBAL_STATIC_DIR_PROD_BUILD='5'

ACTION_DEV_RELOAD_WATCH_LITE='6'
ACTION_DEV_RELOAD_WATCH_NO_FONTS='7'
ACTION_DEV_RELOAD_WATCH_ONLY_PICTURES='8'
ACTION_DEV_RELOAD_WATCH_ALL='9'
ACTION_DEV_BUILD_AND_RELOAD_WATCH_ALL='10'

ACTION_NPM_SHOW_LIST_MODULES='11'
ACTION_CREATE_STRUCTURE_DIR_FOR_APP='12'
ACTION_CREATE_STRUCTURE_DIR_FOR_WIDGET='13'

ACTION_DEV_BUILD_JS='14'
ACTION_DEV_BUILD_CSS='15'
ACTION_DEV_BUILD_IMAGE='16'
ACTION_DEV_BUILD_SVG_SPRITE='17'
ACTION_BUILD_FONTS='18'
ACTION_DEV_BUILD_LITE='19'

ACTION_DEV_BUILD='20'
ACTION_BUILD_PROD='21'

ACTION_DEV_BUILD_SEPARATION_JS='22'
ACTION_DEV_BUILD_SEPARATION_CSS='23'

ACTION_DEV_BUILD_SEPARATION='24'
ACTION_BUILD_PROD_SEPARATION='25'

action=''

npm_start(){
    echo "Are you sure want to NPM start? This may take a long time. [Y/N]"
    
    answer='N'
    read answer

    if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
        npm start
    fi
}

createStructDirApp(){

    appName="$1"
    isCreateDirFonts="$2"

    echo "$appName"

    if [  -d "./$appName" ]; then
        cd "$appName"

        if [ "$isCreateDirFonts" == "Y" ] || [ "$isCreateDirFonts" == "y" ]; then
            mkdir -p "./res_fonts";
        fi

        mkdir -p "./res_scss";
        mkdir -p "./res_img";
        mkdir -p "./res_svg";

        dir_js="./res_js"
        mkdir -p "$dir_js";
        mkdir -p "$dir_js/header";
        mkdir -p "$dir_js/footer";

        cd ".."
        echo -e "$MESSAGE_SUCCESSFULLY_COMPLETED" 
    else
        echo -e "$COLOR_TEXT_RED App '$appName' not exist!" 
    fi
}
while [ "$action" != "$ACTION_EXIT" ]; do

gulp_action=''

echo $'\n'
echo "Select actions with NPM or gulp:"

echo -e "$COLOR_TEXT_RED[$ACTION_INSTALL_NEED_FOR_GULP] - Install, not in Docker (need sudo) required components for gulp"
echo -e "$COLOR_TEXT_RED[$ACTION_NPM_START] - NPM Start (for install or update from 'package.json')"

echo -e "$COLOR_RESET[$ACTION_CLEAN_GLOBAL_STATIC_DIR] - Clean global static directory (Not dangerous. Fully recovers after build dev or prod)"
echo -e "$COLOR_RESET[$ACTION_CLEAN_GLOBAL_STATIC_DIR_DEV_BUILD] - Clean global static and build dev version"
echo -e "$COLOR_RESET[$ACTION_CLEAN_GLOBAL_STATIC_DIR_PROD_BUILD] - Clean global static and build prod version"

echo -e "$COLOR_TEXT_VIOLET[$ACTION_DEV_RELOAD_WATCH_LITE] - Reload watch dev (only js and css)"
echo -e "$COLOR_TEXT_VIOLET[$ACTION_DEV_RELOAD_WATCH_NO_FONTS] - Reload watch dev (without fonts)"
echo -e "$COLOR_TEXT_VIOLET[$ACTION_DEV_RELOAD_WATCH_ONLY_PICTURES] - Reload watch dev (only pictures)"
echo -e "$COLOR_TEXT_VIOLET[$ACTION_DEV_RELOAD_WATCH_ALL] - Reload watch dev (full)"

echo -e "$COLOR_TEXT_SKY_BLUE[$ACTION_DEV_BUILD_AND_RELOAD_WATCH_ALL] - Build dev (full) and reload watch dev (full)"

echo -e "$COLOR_TEXT_VIOLET[$ACTION_NPM_SHOW_LIST_MODULES] - Show list of installed packages"

echo -e "$COLOR_TEXT_GREEN[$ACTION_CREATE_STRUCTURE_DIR_FOR_APP] - Create structure directory for app"
echo -e "$COLOR_TEXT_GREEN[$ACTION_CREATE_STRUCTURE_DIR_FOR_WIDGET] - Create structure directory for widget"

echo -e "$COLOR_TEXT_YELLOW[$ACTION_DEV_BUILD_JS] - Build only js (dev)"

echo -e "$COLOR_TEXT_YELLOW[$ACTION_DEV_BUILD_CSS] - Build only css (dev)"
echo -e "$COLOR_TEXT_YELLOW[$ACTION_DEV_BUILD_IMAGE] - Build only images (dev)"
echo -e "$COLOR_TEXT_YELLOW[$ACTION_DEV_BUILD_SVG_SPRITE] - Build only svg sprite (dev)"
echo -e "$COLOR_TEXT_YELLOW[$ACTION_BUILD_FONTS] - Build only fonts (for all)"
echo -e "$COLOR_TEXT_YELLOW[$ACTION_DEV_BUILD_LITE] - Build lite dev version (rebuild only js and css)"

echo -e "$COLOR_TEXT_SKY_BLUE[$ACTION_DEV_BUILD] - Build dev version"
echo -e "$COLOR_TEXT_GREEN[$ACTION_BUILD_PROD] - Build prod version"

echo -e "$COLOR_RESET[$ACTION_DEV_BUILD_SEPARATION_JS] - Build only js (dev separation static)"
echo -e "$COLOR_RESET[$ACTION_DEV_BUILD_SEPARATION_CSS] - Build only css (dev separation static)"

echo -e "$COLOR_TEXT_SKY_BLUE[$ACTION_DEV_BUILD_SEPARATION] - Build dev version (separation static)"
echo -e "$COLOR_TEXT_GREEN[$ACTION_BUILD_PROD_SEPARATION] - Build prod version (separation static)"

echo -e "$COLOR_RESET[$ACTION_EXIT] - exit"

echo $'\n'

read action

if [ "$action" == "$ACTION_INSTALL_NEED_FOR_GULP" ]; then

    echo "Are you sure want to install components for Gulp? This may take a long time. [Y/N]"
    answer='N'
    read answer

    if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then

        echo "Are you sure want apt update? [Y/N]"
        answer='N'
        read answer

        if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
            sudo apt update
        fi

        echo "Are you sure want add rerository nodejs in your system? [Y/N]"
        answer='N'
        read answer

        if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        fi

        echo "Are you sure want to install nodejs (v 18.x)? [Y/N]"
        answer='N'
        read answer

        if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
            sudo apt-get -y install nodejs
        fi

        echo "Are you sure want to install npm? [Y/N]"
        answer='N'
        read answer

        if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
            sudo apt-get -y install npm
        fi

        echo "Are you sure want to install gulp-cli? [Y/N]"
        answer='N'
        read answer

        if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
            sudo npm install -g gulp-cli
            npm_start
        fi

    fi
elif [ "$action" == "$ACTION_NPM_START" ]; then
    npm_start
    
elif [ "$action" == "$ACTION_NPM_SHOW_LIST_MODULES" ]; then

    echo $'\n'
    echo -e "$COLOR_RESET[L] Show local packages"
    echo -e "[G] Show global packages"

    answer=''
    read answer

    if [ "$answer" == "G" ] || [ "$answer" == "g" ]; then
        npm list -g
    else
        npm list
    fi

elif [ "$action" == "$ACTION_CREATE_STRUCTURE_DIR_FOR_WIDGET" ]; then
    echo "Enter name widget: "
    read widgetName
    createStructDirApp "widget_$widgetName" "N"

elif [ "$action" == "$ACTION_CREATE_STRUCTURE_DIR_FOR_APP" ]; then
    echo "Enter name app: "
    read appName

    isCreateDirFonts='N'
    echo "Create fonts folder (default [N]): [Y/N]"
    read isCreateDirFonts

    createStructDirApp "$appName" isCreateDirFonts

elif [ "$action" == "$ACTION_BUILD_FONTS" ]; then
    gulp_action='fonts'
elif [ "$action" == "$ACTION_DEV_BUILD_CSS" ]; then
    gulp_action='dev-css'
elif [ "$action" == "$ACTION_DEV_BUILD_IMAGE" ]; then
    gulp_action='dev-image'
elif [ "$action" == "$ACTION_DEV_BUILD_SEPARATION_CSS" ]; then
    gulp_action='dev-css-separation'
elif [ "$action" == "$ACTION_DEV_BUILD_SEPARATION_JS" ]; then
    gulp_action='dev-scripts-separation'
elif [ "$action" == "$ACTION_DEV_BUILD_JS" ]; then
    gulp_action='dev-scripts'
elif [ "$action" == "$ACTION_DEV_BUILD_SVG_SPRITE" ]; then
    gulp_action='dev-svg-sprite'
elif [ "$action" == "$ACTION_DEV_BUILD_LITE" ]; then
    gulp_action='dev-build-lite'

elif [ "$action" == "$ACTION_DEV_BUILD_SEPARATION" ]; then
    gulp_action='dev-build-separation'
elif [ "$action" == "$ACTION_BUILD_PROD_SEPARATION" ]; then
    gulp_action='prod-build-separation'

elif [ "$action" == "$ACTION_DEV_BUILD" ]; then
    gulp_action='dev-build'
elif [ "$action" == "$ACTION_BUILD_PROD" ]; then
    gulp_action='prod-build'

elif [ "$action" == "$ACTION_CLEAN_GLOBAL_STATIC_DIR" ]; then
    gulp_action='clean'

elif [ "$action" == "$ACTION_CLEAN_GLOBAL_STATIC_DIR_DEV_BUILD" ]; then
    gulp_action='clean-and-build-dev'
elif [ "$action" == "$ACTION_CLEAN_GLOBAL_STATIC_DIR_PROD_BUILD" ]; then
    gulp_action='clean-and-build-prod'

elif [ "$action" == "$ACTION_DEV_RELOAD_WATCH_LITE" ]; then
    gulp_action='reload-watch-lite'
elif [ "$action" == "$ACTION_DEV_RELOAD_WATCH_NO_FONTS" ]; then
    gulp_action='reload-watch-no-fonts'
elif [ "$action" == "$ACTION_DEV_RELOAD_WATCH_ONLY_PICTURES" ]; then
    gulp_action='reload-watch-only-pictures'
elif [ "$action" == "$ACTION_DEV_RELOAD_WATCH_ALL" ]; then
    gulp_action='reload-watch-all'

elif [ "$action" == "$ACTION_DEV_BUILD_AND_RELOAD_WATCH_ALL" ]; then
    gulp_action='dev-build-reload-watch-all'
fi

if [ "$gulp_action" != "" ]; then

    if [ "$USE_GULP_FROM_DOCKER" != false ]; then
        eval "$RUN_CONTAINER" gulp "$gulp_action"
    else
        eval gulp "$gulp_action"
    fi
    
    gulp_action=''
fi

if [ "$action" != "$ACTION_EXIT" ]; then
    action=''
    echo "Press enter to continue..."
    read press_key_continue
fi

echo -e "$COLOR_RESET"
done