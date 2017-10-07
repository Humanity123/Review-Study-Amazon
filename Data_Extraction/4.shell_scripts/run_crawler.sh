#!/bin/bash
set -x

CURRENT_DIREC=$(pwd)
PROJECT_DIREC=$(pwd)/".."

LINK_SCRIPT_DIREC=$PROJECT_DIREC/"1.product_links"
METADATA_SCRIPT_DIREC=$PROJECT_DIREC/"2.product_metadata"
REVIEW_SCRIPT_DIREC=$PROJECT_DIREC/"3.reviews"

LINK_INDIA_SCRIPT=$LINK_SCRIPT_DIREC/"links_in.py"
LINK_USA_SCRIPT=$LINK_SCRIPT_DIREC/"links_com.py"
LINK_UK_SCRIPT=$LINK_SCRIPT_DIREC/"links_uk.py"

METADATA_INDIA_SCRIPT=$METADATA_SCRIPT_DIREC/"products_in.py"
METADATA_USA_SCRIPT=$METADATA_SCRIPT_DIREC/"products_com.py"
METADATA_UK_SCRIPT=$METADATA_SCRIPT_DIREC/"products_uk.py"

REVIEW_INDIA_SCRIPT=$REVIEW_SCRIPT_DIREC/"reviews_in.py"
REVIEW_USA_SCRIPT=$REVIEW_SCRIPT_DIREC/"reviews_com.py"
REVIEW_UK_SCRIPT=$REVIEW_SCRIPT_DIREC/"reviews_uk.py"

LOG_FILE_DIREC=$PROJECT_DIREC/"../log_files"

[ -d $LOG_FILE_DIREC ] || mkdir $LOG_FILE_DIREC

LOG_FILE_INDIA=$LOG_FILE_DIREC/"log_in.out"
LOG_FILE_USA=$LOG_FILE_DIREC/"log_com.out"
LOG_FILE_UK=$LOG_FILE_DIREC/"log_uk.out"

DATABASE_DIREC="../../../data"
DATABASE_DIREC_INDIA=$DATABASE_DIREC/"in"
DATABASE_DIREC_USA=$DATABASE_DIREC/"us"
DATABASE_DIREC_UK=$DATABASE_DIREC/"uk"

SHELL_SCRIPT_DIREC=$PROJECT_DIREC/"4.shell_scripts"
COLLECT_DATA_SCRIPT=$SHELL_SCRIPT_DIREC/"collect_data.sh"
MAILING_SCRIPT=$SHELL_SCRIPT_DIREC/"mail_progess_report.sh"
MAILING_ADDRESS="kushagra.iitkgp@iitkgp.ac.in"

crontab -l > cronjobs
# echo "* 1 * * * $MAILING_SCRIPT $LOG_FILE_INDIA > /dev/null 2>&1" >> cronjobs
# echo "* 1 * * * $MAILING_SCRIPT $LOG_FILE_USA > /dev/null 2>&1" >> cronjobs
# echo "* 1 * * * $MAILING_SCRIPT $LOG_FILE_UK > /dev/null 2>&1" >> cronjobs

# echo "*/5 * * * * ./clean_server.sh" >> cronjob
crontab cronjobs
# crontab cronjob

# $COLLECT_DATA_SCRIPT INDIA $DATABASE_DIREC_INDIA &
$COLLECT_DATA_SCRIPT USA $DATABASE_DIREC_USA  	&
# $COLLECT_DATA_SCRIPT UK $DATABASE_DIREC_UK   	&
wait

rm cronjobs