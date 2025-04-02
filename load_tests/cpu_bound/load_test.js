import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
	// Key configurations for Stress in this section
	stages: [
		{ duration: "1m", target: 400 }, // traffic ramp-up from 1 to a higher 400 users over 1 minutes.
		{ duration: "5m", target: 400 }, // stay at higher 400 users for 5 minutes
		{ duration: "1m", target: 0 }, // ramp-down to 0 users
	],
};

export default function () {
	// Generate a random number for the factorial calculation
	const number = Math.floor(Math.random() * 20) + 1; // Factorial of numbers between 1 and 20

	// Send a GET request to the /calculate-factorial/{number} endpoint
	const res = http.get(`http://localhost:3000/calculate-factorial/${number}`);

	// Perform checks to validate the response
	check(res, {
		"status is 200": (r) => r.status === 200,
		"response contains result": (r) => JSON.parse(r.body).hasOwnProperty("result"),
	});

	sleep(1); // Sleep before next iteration
}
