test=$1 # smoke load spike breakpoint
s=$2 # time to wait between tests

run_tests ()
{
  local log_file="logs/$1"
  echo -e "\n--------test IO and CPU bound------------\n" | tee -a $log_file

  k6 run load_tests/io_cpu_bound/${test}_test.js | tee -a $log_file
  sleep ${s}

  echo -e "\n--------test IO bound------------\n" | tee -a $log_file

  k6 run load_tests/io_bound/${test}_test.js | tee -a $log_file
  sleep ${s}


  echo -e "\n--------test CPU bound------------\n" | tee -a $log_file

  k6 run load_tests/cpu_bound/${test}_test.js | tee -a $log_file
  sleep ${s}
}

run_servers () {
  local server_type=$1 # sync or async
  local log_file_name_extension=$2 # optional
  local log_file="logs/${server_type}_server_{$log_file_name_extension}.log"
  echo "------------start ${server_type} server------------"
  uvicorn servers.${server_type}_server:app --host 127.0.0.1 --port 3000 > log_file 2>&1 &
  SYNC_SERVER_PID=$!

  sleep 5 # wait for the server to start

  echo -e "\n------------running ${test} tests------------ $(date)\n"
  run_tests ${server_type}_server_{$log_file_name_extension}_tests.log
  echo -e "\n------------tests finished------------ $(date)\n"

  echo -e "\n------------stop ${server_type} server------------\n"
  kill ${SYNC_SERVER_PID}

  sleep 5 # wait for the server to stop
}

echo -e "\nmake you run this script from the project root directory"
echo -e "make sure you activate the venv: source .venv/bin/activate\n"

if [ ! -d "logs" ]; then mkdir logs; fi

# first use
# run_servers "sync"
# run_servers "async"

# second use
run_servers "async" "httptools_uvloop"


echo "------------Done :)------------"
