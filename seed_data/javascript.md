# Modern JavaScript Tutorial

The Modern JavaScript Tutorial is a comprehensive, open-source educational resource covering JavaScript from fundamentals to advanced concepts. It provides in-depth explanations of the JavaScript language, browser APIs, DOM manipulation, asynchronous programming, and network communication. The tutorial is designed for developers at all skill levels, progressing from basic syntax through complex patterns like closures, promises, and modern ES6+ features.

The tutorial is organized into logical sections covering core JavaScript language features, browser document interaction (DOM/BOM), events handling, network requests, data storage, animations, web components, and regular expressions. Each topic includes detailed explanations, interactive code examples, and practical exercises. The content emphasizes real-world usage patterns and best practices while explaining the underlying mechanics of how JavaScript works.

## Variables and Data Types

JavaScript supports multiple ways to declare variables with `let`, `const`, and the legacy `var`. Variables declared with `let` and `const` are block-scoped and cannot be redeclared, while `const` additionally prevents reassignment. JavaScript has eight basic data types including primitives (string, number, bigint, boolean, undefined, symbol, null) and objects.

```javascript
// Variable declarations
let message = "Hello";
const PI = 3.14159;
let age = 25;

// Data types
let str = "text"; // string
let num = 42; // number
let bigNum = 9007199254740991n; // bigint
let isActive = true; // boolean
let nothing = null; // null (intentional absence)
let notDefined; // undefined
let id = Symbol("id"); // symbol

// Type checking
console.log(typeof str); // "string"
console.log(typeof num); // "number"
console.log(typeof isActive); // "boolean"
console.log(typeof nothing); // "object" (historical bug)
console.log(typeof notDefined); // "undefined"
```

## Objects

Objects store keyed collections of data and more complex entities. They can be created using object literal syntax `{}` or the `new Object()` constructor. Properties can be accessed using dot notation or square brackets, and can be dynamically added, modified, or deleted.

```javascript
// Creating objects
let user = {
  name: "John",
  age: 30,
  "likes birds": true, // multiword property
};

// Accessing properties
console.log(user.name); // "John"
console.log(user["likes birds"]); // true

// Adding and modifying properties
user.isAdmin = true;
user.age = 31;

// Deleting properties
delete user["likes birds"];

// Property existence check
console.log("name" in user); // true
console.log("email" in user); // false

// Iterating over properties
for (let key in user) {
  console.log(`${key}: ${user[key]}`);
}
// Output: name: John, age: 31, isAdmin: true

// Computed properties
let fruit = "apple";
let bag = {
  [fruit]: 5, // property name from variable
};
console.log(bag.apple); // 5

// Property shorthand
function makeUser(name, age) {
  return { name, age }; // same as { name: name, age: age }
}
```

## Arrays

Arrays are special objects for storing ordered collections. They provide methods for adding, removing, and manipulating elements at both ends. Arrays support iteration with `for`, `for..of`, and various built-in methods.

```javascript
// Creating arrays
let fruits = ["Apple", "Orange", "Plum"];

// Accessing elements
console.log(fruits[0]); // "Apple"
console.log(fruits.at(-1)); // "Plum" (last element)
console.log(fruits.length); // 3

// Modifying arrays
fruits[2] = "Pear"; // replace element
fruits[3] = "Lemon"; // add element

// Stack operations (end of array)
fruits.push("Banana"); // add to end
let last = fruits.pop(); // remove from end, returns "Banana"

// Queue operations (beginning of array)
fruits.unshift("Grape"); // add to beginning
let first = fruits.shift(); // remove from beginning, returns "Grape"

// Iterating
for (let fruit of fruits) {
  console.log(fruit);
}

// Mixed types
let arr = [
  "Apple",
  { name: "John" },
  true,
  function () {
    alert("hello");
  },
];
console.log(arr[1].name); // "John"
arr[3](); // alerts "hello"

// Multidimensional arrays
let matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];
console.log(matrix[1][1]); // 5
```

## Functions

Functions are the main building blocks of JavaScript programs. They can be declared using function declarations, function expressions, or arrow function syntax. Functions can accept parameters, return values, and access variables from their outer scope (closure).

```javascript
// Function declaration
function greet(name) {
  return `Hello, ${name}!`;
}
console.log(greet("John")); // "Hello, John!"

// Function expression
let sayHi = function (name) {
  console.log(`Hi, ${name}!`);
};
sayHi("Jane"); // "Hi, Jane!"

// Arrow functions
let sum = (a, b) => a + b;
console.log(sum(1, 2)); // 3

let double = (n) => n * 2; // single parameter, no parentheses needed
console.log(double(5)); // 10

// Default parameters
function showMessage(from, text = "no text given") {
  console.log(`${from}: ${text}`);
}
showMessage("Ann"); // "Ann: no text given"

// Rest parameters
function sumAll(...numbers) {
  let total = 0;
  for (let n of numbers) total += n;
  return total;
}
console.log(sumAll(1, 2, 3, 4)); // 10

// Nested functions and closures
function makeCounter() {
  let count = 0;
  return function () {
    return count++;
  };
}
let counter = makeCounter();
console.log(counter()); // 0
console.log(counter()); // 1
console.log(counter()); // 2
```

## Closures

A closure is a function that remembers its outer variables and can access them. In JavaScript, all functions are naturally closures - they automatically remember where they were created using a hidden `[[Environment]]` property and can access outer variables.

```javascript
// Closure example - counter factory
function makeCounter() {
  let count = 0;

  return function () {
    return count++; // accesses 'count' from outer scope
  };
}

let counter1 = makeCounter();
let counter2 = makeCounter();

console.log(counter1()); // 0
console.log(counter1()); // 1
console.log(counter2()); // 0 (independent counter)

// Closure for private variables
function createUser(name) {
  let _password = ""; // private variable

  return {
    getName: () => name,
    setPassword: (pwd) => {
      _password = pwd;
    },
    checkPassword: (pwd) => pwd === _password,
  };
}

let user = createUser("John");
user.setPassword("secret123");
console.log(user.checkPassword("secret123")); // true
console.log(user.checkPassword("wrong")); // false
// console.log(user._password);  // undefined (not accessible)

// Closure in loops (common gotcha and solution)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2 (let creates new binding for each iteration)
```

## Promises

Promises provide a way to handle asynchronous operations. A Promise object represents the eventual completion (or failure) of an async operation and its resulting value. Promises have three states: pending, fulfilled, or rejected.

```javascript
// Creating a promise
let promise = new Promise((resolve, reject) => {
  // Async operation
  setTimeout(() => {
    let success = true;
    if (success) {
      resolve("Operation completed!");
    } else {
      reject(new Error("Operation failed!"));
    }
  }, 1000);
});

// Consuming a promise with .then() and .catch()
promise
  .then((result) => console.log(result)) // "Operation completed!"
  .catch((error) => console.log(error.message))
  .finally(() => console.log("Cleanup"));

// Promise chaining
function loadScript(src) {
  return new Promise((resolve, reject) => {
    let script = document.createElement("script");
    script.src = src;
    script.onload = () => resolve(script);
    script.onerror = () => reject(new Error(`Script load error: ${src}`));
    document.head.append(script);
  });
}

loadScript("/script1.js")
  .then((script) => {
    console.log(`${script.src} loaded`);
    return loadScript("/script2.js");
  })
  .then((script) => console.log(`${script.src} loaded`))
  .catch((err) => console.log(err.message));

// Promise.all - wait for all promises
Promise.all([
  fetch("/api/users"),
  fetch("/api/posts"),
  fetch("/api/comments"),
]).then((responses) => {
  console.log("All requests completed");
});

// Promise.race - first to complete wins
Promise.race([
  fetch("/api/fast"),
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), 5000),
  ),
]).then((response) => console.log("Got response before timeout"));
```

## Async/Await

Async/await is syntactic sugar over Promises that makes asynchronous code look and behave more like synchronous code. The `async` keyword makes a function return a Promise, and `await` pauses execution until a Promise settles.

```javascript
// Basic async/await
async function fetchUser() {
  let response = await fetch("/api/user");
  let user = await response.json();
  return user;
}

fetchUser().then((user) => console.log(user.name));

// Error handling with try/catch
async function fetchData() {
  try {
    let response = await fetch("http://no-such-url");
    let data = await response.json();
    return data;
  } catch (err) {
    console.log("Fetch failed:", err.message);
    return null;
  }
}

// Sequential vs parallel execution
async function loadSequential() {
  let user = await fetch("/api/user").then((r) => r.json());
  let posts = await fetch("/api/posts").then((r) => r.json());
  return { user, posts }; // Takes time of user + posts
}

async function loadParallel() {
  let [user, posts] = await Promise.all([
    fetch("/api/user").then((r) => r.json()),
    fetch("/api/posts").then((r) => r.json()),
  ]);
  return { user, posts }; // Takes time of max(user, posts)
}

// Real-world example: fetching and displaying data
async function showAvatar() {
  let response = await fetch("/api/user");
  let user = await response.json();

  let githubResponse = await fetch(`https://api.github.com/users/${user.name}`);
  let githubUser = await githubResponse.json();

  let img = document.createElement("img");
  img.src = githubUser.avatar_url;
  document.body.append(img);

  await new Promise((resolve) => setTimeout(resolve, 3000));
  img.remove();

  return githubUser;
}
```

## Fetch API

The Fetch API provides a modern interface for making HTTP requests. It returns Promises and supports various request methods, headers, and body formats. Response data can be read as JSON, text, blob, or other formats.

```javascript
// Basic GET request
let response = await fetch(
  "https://api.github.com/repos/javascript-tutorial/en.javascript.info/commits",
);
let commits = await response.json();
console.log(commits[0].author.login);

// With promise syntax
fetch("https://api.github.com/users/octocat")
  .then((response) => response.json())
  .then((user) => console.log(user.name));

// Checking response status
let response = await fetch(url);
if (response.ok) {
  let json = await response.json();
} else {
  console.log("HTTP-Error: " + response.status);
}

// POST request with JSON body
let user = { name: "John", surname: "Smith" };

let response = await fetch("/api/users", {
  method: "POST",
  headers: {
    "Content-Type": "application/json;charset=utf-8",
  },
  body: JSON.stringify(user),
});

let result = await response.json();
console.log(result.message);

// Sending FormData
let formData = new FormData();
formData.append("name", "John");
formData.append("file", fileInput.files[0]);

let response = await fetch("/api/upload", {
  method: "POST",
  body: formData, // Content-Type is set automatically
});

// Reading response headers
let response = await fetch(url);
console.log(response.headers.get("Content-Type"));

for (let [key, value] of response.headers) {
  console.log(`${key} = ${value}`);
}

// Downloading binary data (image)
let response = await fetch("/logo.png");
let blob = await response.blob();
let img = document.createElement("img");
img.src = URL.createObjectURL(blob);
document.body.append(img);
```

## DOM Manipulation

The Document Object Model (DOM) provides methods to create, modify, and remove elements from a webpage. Modern methods like `append`, `prepend`, `before`, `after`, and `remove` make DOM manipulation straightforward.

```javascript
// Creating elements
let div = document.createElement("div");
div.className = "alert";
div.innerHTML = "<strong>Hi!</strong> Important message.";

// Inserting elements
document.body.append(div); // at the end of body
document.body.prepend(div); // at the beginning of body
someElement.before(div); // before someElement
someElement.after(div); // after someElement
someElement.replaceWith(div); // replace someElement

// Removing elements
div.remove();

// insertAdjacentHTML - insert HTML string
div.insertAdjacentHTML("beforebegin", "<p>Before</p>"); // before div
div.insertAdjacentHTML("afterbegin", "<p>First child</p>"); // first child
div.insertAdjacentHTML("beforeend", "<p>Last child</p>"); // last child
div.insertAdjacentHTML("afterend", "<p>After</p>"); // after div

// Cloning elements
let div2 = div.cloneNode(true); // deep clone with all children
let div3 = div.cloneNode(false); // shallow clone without children

// Searching for elements
let element = document.getElementById("id");
let elements = document.querySelectorAll(".class");
let first = document.querySelector(".class");
let byClass = document.getElementsByClassName("class");
let byTag = document.getElementsByTagName("div");

// Modifying content
element.textContent = "Plain text"; // text only
element.innerHTML = "<b>HTML</b> content"; // parsed HTML

// Modifying attributes
element.setAttribute("data-id", "123");
element.getAttribute("data-id"); // "123"
element.removeAttribute("data-id");
element.dataset.id = "456"; // data-id="456"

// Modifying styles
element.style.backgroundColor = "red";
element.style.cssText = "color: blue; font-size: 14px;";
element.classList.add("active");
element.classList.remove("active");
element.classList.toggle("active");
```

## Event Handling

Events allow JavaScript to react to user actions and browser occurrences. Handlers can be assigned using HTML attributes, DOM properties, or the `addEventListener` method which allows multiple handlers per event.

```javascript
// DOM property handler
element.onclick = function (event) {
  console.log("Clicked!");
  console.log("Event type:", event.type);
  console.log("Target element:", event.target);
  console.log("Coordinates:", event.clientX, event.clientY);
};

// addEventListener (recommended)
function handleClick(event) {
  console.log("Clicked:", event.target);
}

element.addEventListener("click", handleClick);
element.removeEventListener("click", handleClick);

// Multiple handlers
element.addEventListener("click", () => console.log("Handler 1"));
element.addEventListener("click", () => console.log("Handler 2"));

// Event options
element.addEventListener("click", handler, {
  once: true, // auto-remove after first trigger
  capture: true, // handle during capture phase
  passive: true, // handler won't call preventDefault()
});

// Common events
element.addEventListener("click", handler); // mouse click
element.addEventListener("dblclick", handler); // double click
element.addEventListener("mousedown", handler); // mouse button pressed
element.addEventListener("mouseup", handler); // mouse button released
element.addEventListener("mousemove", handler); // mouse moved
element.addEventListener("keydown", handler); // key pressed
element.addEventListener("keyup", handler); // key released
element.addEventListener("submit", handler); // form submitted
element.addEventListener("focus", handler); // element focused
element.addEventListener("blur", handler); // element lost focus

// Event delegation
document.addEventListener("click", function (event) {
  if (event.target.matches(".btn")) {
    console.log("Button clicked:", event.target.textContent);
  }
});

// Preventing default behavior
form.addEventListener("submit", function (event) {
  event.preventDefault(); // prevent form submission
  // custom handling
});

// DOMContentLoaded - DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");
});
```

## LocalStorage and SessionStorage

Web Storage provides `localStorage` and `sessionStorage` objects for storing key/value pairs in the browser. `localStorage` persists across browser sessions while `sessionStorage` is limited to the current tab session.

```javascript
// localStorage - persists across sessions
localStorage.setItem("username", "John");
let username = localStorage.getItem("username"); // "John"
localStorage.removeItem("username");
localStorage.clear(); // remove all items

// Storing objects (must stringify)
let user = { name: "John", age: 30 };
localStorage.setItem("user", JSON.stringify(user));
let retrieved = JSON.parse(localStorage.getItem("user"));
console.log(retrieved.name); // "John"

// sessionStorage - tab-specific, survives refresh
sessionStorage.setItem("tempData", "value");
let temp = sessionStorage.getItem("tempData");

// Iterating over storage
for (let i = 0; i < localStorage.length; i++) {
  let key = localStorage.key(i);
  console.log(`${key}: ${localStorage.getItem(key)}`);
}

// Using Object.keys
let keys = Object.keys(localStorage);
for (let key of keys) {
  console.log(`${key}: ${localStorage.getItem(key)}`);
}

// Storage event (fires in other tabs/windows)
window.addEventListener("storage", function (event) {
  console.log("Storage changed:");
  console.log("Key:", event.key);
  console.log("Old value:", event.oldValue);
  console.log("New value:", event.newValue);
  console.log("URL:", event.url);
});

// Practical example: form auto-save
const textarea = document.querySelector("textarea");

textarea.value = localStorage.getItem("draft") || "";

textarea.addEventListener("input", function () {
  localStorage.setItem("draft", this.value);
});
```

## Classes

ES6 classes provide a cleaner syntax for object-oriented programming in JavaScript. Classes support constructors, methods, static members, getters/setters, and inheritance via the `extends` keyword.

```javascript
// Class declaration
class User {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  // Method
  sayHi() {
    console.log(`Hi, I'm ${this.name}`);
  }

  // Getter
  get info() {
    return `${this.name}, ${this.age} years old`;
  }

  // Setter
  set info(value) {
    [this.name, this.age] = value.split(", ");
  }

  // Static method
  static createAnonymous() {
    return new User("Anonymous", 0);
  }
}

let user = new User("John", 30);
user.sayHi(); // "Hi, I'm John"
console.log(user.info); // "John, 30 years old"
User.createAnonymous(); // Creates anonymous user

// Inheritance
class Admin extends User {
  constructor(name, age, permissions) {
    super(name, age); // call parent constructor
    this.permissions = permissions;
  }

  sayHi() {
    super.sayHi(); // call parent method
    console.log(`I have ${this.permissions.length} permissions`);
  }
}

let admin = new Admin("Jane", 25, ["read", "write", "delete"]);
admin.sayHi();
// "Hi, I'm Jane"
// "I have 3 permissions"

// Private fields (ES2022)
class BankAccount {
  #balance = 0; // private field

  deposit(amount) {
    this.#balance += amount;
  }

  getBalance() {
    return this.#balance;
  }
}
```

## Error Handling

JavaScript provides `try...catch...finally` for handling runtime errors. Custom error classes can extend the built-in `Error` class for domain-specific error handling.

```javascript
// Basic try/catch
try {
  let result = someFunction();
} catch (err) {
  console.log("Error name:", err.name);
  console.log("Error message:", err.message);
  console.log("Stack trace:", err.stack);
} finally {
  console.log("This always runs");
}

// Throwing errors
function divide(a, b) {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

try {
  divide(10, 0);
} catch (err) {
  console.log(err.message); // "Division by zero"
}

// Custom error classes
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

class PropertyRequiredError extends ValidationError {
  constructor(property) {
    super(`Missing property: ${property}`);
    this.name = "PropertyRequiredError";
    this.property = property;
  }
}

function validateUser(user) {
  if (!user.name) {
    throw new PropertyRequiredError("name");
  }
  if (!user.age) {
    throw new PropertyRequiredError("age");
  }
}

try {
  validateUser({ name: "John" });
} catch (err) {
  if (err instanceof PropertyRequiredError) {
    console.log(`Property required: ${err.property}`);
  } else {
    throw err; // re-throw unknown errors
  }
}
```

## Summary

The Modern JavaScript Tutorial serves as a comprehensive reference for JavaScript developers, covering everything from basic syntax to advanced patterns. It is particularly valuable for learning core language concepts like closures, prototypes, and the event loop, as well as practical browser APIs for DOM manipulation, event handling, network requests, and data storage.

The tutorial's strength lies in its progressive approach - concepts build upon each other, allowing developers to deepen their understanding incrementally. For integration into existing projects, the code examples demonstrate modern best practices including ES6+ features, async/await patterns, and proper error handling. Developers can use these patterns for building interactive web applications, handling user input, making API calls, and managing application state in the browser.
