if [[ -z "${PRODUCTION}" ]]; then
  echo "RUNNING PRODUCTION"
   export SETTINGS_PATH='settings.production'
  bash /manage/prod_run.sh
else
  echo "RUNNING DEVELOPMENT"
  export SETTINGS_PATH='settings.development'
  bash /manage/dev_run.sh
fi