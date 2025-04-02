import http from "k6/http";
import { check, sleep } from "k6";

// Define options for the test run
export const options = {
  stages: [
    { duration: "30s", target: 100 }, // Ramp up to 100 users over 30 seconds
    { duration: "2m", target: 300 }, // Stay at 200 users for 2 minutes
    { duration: "30s", target: 0 }, // Ramp down to 0 users
  ],
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

