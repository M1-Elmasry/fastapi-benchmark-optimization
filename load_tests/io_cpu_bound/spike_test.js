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
	// Generate a random number for the factorial calculation
	const number = Math.floor(Math.random() * 50000) + 1; // Factorial of numbers between 1 and 50000

	// Send a GET request to the /calculate-factorial/{number} endpoint
	const res = http.get(`http://localhost:3000/employee-exp-factorial/${number}`);

	// Perform checks to validate the response
	check(res, {
		"status is 200": (r) => r.status === 200,
		"response contains result or employee not found": (r) => {
    const res = JSON.parse(r.body);
    return res.hasOwnProperty("result") || res.message === "employee not found";
    },
	});
	sleep(1); // Sleep before next iteration
}
