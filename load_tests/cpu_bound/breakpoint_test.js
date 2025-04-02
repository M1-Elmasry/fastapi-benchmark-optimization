import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
	stages: [
		{ duration: "3m", target: 500 }, // Ramp up to 500 users
		{ duration: "5m", target: 700 }, // Ramp up to 700 users
		{ duration: "5m", target: 1000 }, // Ramp up to 1000 users
		{ duration: "30m", target: 20000 }, // Ramp up until break
	],
};

export default function () {
	// Generate a random number for the factorial calculation
	const number = Math.floor(Math.random() * 20) + 1; // Factorial of numbers between 1 and 20 for quick stress

	// Send a GET request to the /calculate-factorial/{number} endpoint
	const res = http.get(`http://localhost:3000/calculate-factorial/${number}`);

	// Perform checks to validate the response
	check(res, {
		"status is 200": (r) => r.status === 200, // Check if the status is 200
		"response contains result": (r) => JSON.parse(r.body).hasOwnProperty("result"), // Check if the result is included in the response
	});

	sleep(1); // Sleep for a second before next request
}
