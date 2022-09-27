#!/bin/bash
. ./scripts_config.sh

#=================================Global actions===================================
ACTION_EXIT='0'

ACTION_IMPORT_ALL_DB='1'
ACTION_EXPORT_ALL_DB_FROM_BACKUP='2'

ACTION_DJANGO_CREATE_APP='3'
ACTION_DJANGO_CREATE_WIDGET='4'

ACTION_DJANGO_MAKE_MIGRATIONS='5'
ACTION_DJANGO_APPLY_MIGRATIONS='6'
ACTION_DJANGO_MAKE_APPLY_MIGRATIONS='7'

ACTION_REGISTRATION_IN_DJANGO_ADMINISTRATION='8'

DOCKER_USE_NPM_OR_GULP='9'

DOCKER_COMPOSE_REBUILD='10'
DOCKER_COMPOSE_UP='11'
DOCKER_COMPOSE_DOWN='12'

COLLECT_STATIC_FOR_PROD='13'
RUN_TESTS='14'
#=================================End global actions===============================

DIRS=(
    "$DIR_BACKUP"
)

initDirs(){
    for i in "${DIRS[@]}"
    do
        echo "$i"
        if [ ! -d "$i" ]; then
            mkdir -p "$i";
        fi
    done
}

makeMigrations(){
    echo "Enter name migration app: "
    name_table=''
    read name_table
    eval "$MANAGER_PY" makemigrations "$name_table"
}

applyMigrations(){
    eval "$MANAGER_PY" migrate
}

initDirs

select_do=''
current_date=''
press_key_continue=''

while [ "$select_do" != "$ACTION_EXIT" ]; do

    echo $'\n'
	echo "Actions with Djangon in DOCKER:"

    echo -e "$COLOR_TEXT_SKY_BLUE[$ACTION_IMPORT_ALL_DB] - import all Data base"
    echo -e "$COLOR_TEXT_SKY_BLUE[$ACTION_EXPORT_ALL_DB_FROM_BACKUP] - export all Data from backup"
    
    echo -e "$COLOR_TEXT_GREEN[$ACTION_DJANGO_CREATE_APP] - Django create app"
    echo -e "$COLOR_TEXT_GREEN[$ACTION_DJANGO_CREATE_WIDGET] - Create widget (base django app)"

    echo -e "$COLOR_TEXT_YELLOW[$ACTION_DJANGO_MAKE_MIGRATIONS] - Django make migrations"
    echo -e "$COLOR_TEXT_YELLOW[$ACTION_DJANGO_APPLY_MIGRATIONS] - Django apply migrations"
    echo -e "$COLOR_TEXT_YELLOW[$ACTION_DJANGO_MAKE_APPLY_MIGRATIONS] - Django make and apply migrations"
    
    echo -e "$COLOR_TEXT_SKY_BLUE[$ACTION_REGISTRATION_IN_DJANGO_ADMINISTRATION] - Registration in Django administration"

    echo -e "$COLOR_TEXT_GREEN[$DOCKER_USE_NPM_OR_GULP] - Use NPM or gulp"

    echo -e "$COLOR_TEXT_RED[$DOCKER_COMPOSE_REBUILD] - Docker-compose rebuild"
    echo -e "$COLOR_TEXT_GREEN[$DOCKER_COMPOSE_UP] - Docker-compose up"
    echo -e "$COLOR_TEXT_YELLOW[$DOCKER_COMPOSE_DOWN] - Docker-compose down"

    echo -e "$COLOR_RESET[$COLLECT_STATIC_FOR_PROD] - Collect static for prod"
    echo -e "$COLOR_TEXT_GREEN[$RUN_TESTS] - Run tests"
    echo -e "$COLOR_RESET[$ACTION_EXIT] - exit"
	echo $'\n'

    echo -n "Select an action: "
	read select_do
    current_date=`date +%Y-%m-%d_%H:%M:%S`


    if [ "$select_do" == "$ACTION_IMPORT_ALL_DB" ]; then
        file="$DIR_BACKUP$DB_PREFIX$current_date".json
        eval "$MANAGER_PY" dumpdata --indent 2 > "$file"
        echo "Created file: $file"
    elif [ "$select_do" == "$ACTION_EXPORT_ALL_DB_FROM_BACKUP" ]; then

        i=0
        cd "$DIR_BACKUP"
        echo "Select backups: "

        for entry in *.json
        do
            array_db[$i]=$entry
            echo "[$i] - $entry"
            let i++
        done

        cd ".."

        echo "Select backup: "
        index_backup=''
        read index_backup
        select_backup=${array_db[index_backup]}

        if [ ${#select_backup} -ne "0" ]; then
 
            echo -e "Selected: $COLOR_TEXT_YELLOW$select_backup$COLOR_RESET"
            eval "$MANAGER_PY" loaddata "$DIR_BACKUP$select_backup"
        else
            echo -e "$COLOR_TEXT_RED Backup with index '$index_backup' not exist!" 
        fi

    elif [ "$select_do" == "$ACTION_DJANGO_CREATE_APP" ]; then
        echo "Enter name app: "
        name_app=''
        read name_app
        eval "$MANAGER_PY" startapp "$name_app"
    elif [ "$select_do" == "$ACTION_DJANGO_CREATE_WIDGET" ]; then
        echo "Enter name widget: "
        name_app=''
        read name_app
        eval "$MANAGER_PY" startapp "widget_$name_app"
    elif [ "$select_do" == "$ACTION_DJANGO_MAKE_MIGRATIONS" ]; then
        makeMigrations
    elif [ "$select_do" == "$ACTION_DJANGO_APPLY_MIGRATIONS" ]; then
        applyMigrations
    elif [ "$select_do" == "$ACTION_DJANGO_MAKE_APPLY_MIGRATIONS" ]; then
        makeMigrations
        applyMigrations
    elif [ "$select_do" == "$RUN_TESTS" ]; then
        eval "$MANAGER_PY test"
    elif [ "$select_do" == "$ACTION_REGISTRATION_IN_DJANGO_ADMINISTRATION" ]; then
        eval "$MANAGER_PY" createsuperuser

    elif [ "$select_do" == "$DOCKER_COMPOSE_UP" ]; then
        docker-compose up
    elif [ "$select_do" == "$DOCKER_COMPOSE_DOWN" ]; then
        docker-compose down
    elif [ "$select_do" == "$DOCKER_COMPOSE_REBUILD" ]; then
       
        echo "Are you sure want to rebuild the project? This may take a long time. [Y/N]"
        
        answer='N'
        read answer

        if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
            docker-compose up -d --build
        fi
    
    elif [ "$select_do" == "$DOCKER_USE_NPM_OR_GULP" ]; then
        bash ./script_npm_gulp.sh
    elif [ "$select_do" == "$COLLECT_STATIC_FOR_PROD" ]; then
        eval "$MANAGER_PY" collectstatic
    else
		echo "Error action!"
    fi

    if [ "$select_do" != "$ACTION_EXIT" ]; then
        select_do=''
        echo "Press enter to continue..."
        read press_key_continue
    fi


done