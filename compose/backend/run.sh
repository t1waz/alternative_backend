if [[ -z "${PRODUCTION}" ]]; then
  echo "RUNNING PRODUCTION"
   export SETTINGS_PATH='settings.production'
  ./prod_run.sh
else
  echo "RUNNING DEVELOPMENT"
  export SETTINGS_PATH='settings.development'
  ./dev_run.sh
fi