test=$1
s=$2

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

echo -e "\nmake you run this script from the project root directory"
echo -e "make sure you activate the venv: source .venv/bin/activate\n"

if [ ! -d "logs" ]; then mkdir logs; fi

echo "------------start synchronous server------------"
uvicorn servers.sync_server:app --host 127.0.0.1 --port 3000 > logs/sync_server.log 2>&1 &
SYNC_SERVER_PID=$!

sleep 5 # wait for the server to start

echo -e "\n------------running ${test} tests------------ $(date)\n"
run_tests sync_server_tests.log
echo -e "\n------------tests finished------------ $(date)\n"

echo -e "\n------------stop synchronous server------------\n"
kill ${SYNC_SERVER_PID}

sleep 5 # wait for the server to stop

echo "------------start asynchronous server------------"
uvicorn servers.async_server:app --host 127.0.0.1 --port 3000 > logs/async_server.log 2>&1 &
ASYNC_SERVER_PID=$!

sleep 5 # wait for the server to start

echo -e "\n------------running ${test} tests------------ $(date)\n"
run_tests async_server_tests.log
echo -e "\n------------tests finished------------ $(date)\n"

echo -e "\n------------stop asynchronous server------------\n"
kill ${ASYNC_SERVER_PID}

sleep 5 # wait for the server to stop

echo "------------Done :)------------"
