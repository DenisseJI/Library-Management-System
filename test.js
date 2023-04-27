const person = {"name":"Andrew", "loves":"Open Source"};
const asJSON = JSON.stringify(person);

// `person` is of type 'object'
console.log(`person is of type ${typeof person}`);

// `asJSON` is of type 'string'
console.log(`asJSON is of type ${typeof asJSON}`);

// We can convert it back to an object by parsing it
// `asObject` is of type 'object'
const asObject = JSON.parse(asJSON);
console.log(`asObject is of type ${typeof asObject}`);