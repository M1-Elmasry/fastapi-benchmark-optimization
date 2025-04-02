import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
	vus: 5, // 5 virtual user
	duration: "5s", // Run for 30 seconds
};

export default function () {
  // Generate a random employee ID between 1 and 50000 (assuming there are 50000 employees)
  const employee_id = Math.floor(Math.random() * 50000) + 1;

  // Send a GET request to the /employees/{employee_id} endpoint
  const res = http.get(`http://localhost:3000/employees/${employee_id}`);

  // Perform checks to validate the response
  check(res, {
    "status is 200": (r) => r.status === 200, // Check if status is 200
    "response contains employee data or not found message": (r) => {
      const responseBody = JSON.parse(r.body);
      return responseBody.hasOwnProperty("id") || responseBody.message === "employee not found";
    },
  });

  sleep(1); // Sleep for 1 second before next iteration
}

