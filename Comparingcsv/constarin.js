function isWithinRange(value, min, max) {
    return value >= min && value <= max;
}

function main() {
    let maxLimit = Math.pow(16, 8);
    let values = [];

    for (let i = 1; i <= maxLimit; i++) {
        if (isWithinRange(i, 1, maxLimit)) {
            values.push(i);
        }
    }

    if (values.length > 0) {
        let lastValue = values[values.length - 1];
        console.log("Last Value: " + lastValue);
    } else {
        console.log("No values within the range.");
    }
}

main();
