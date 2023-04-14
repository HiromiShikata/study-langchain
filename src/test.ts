
function fibonacci(index: number): number {
    if (index < 2) {
        return index;
    }
    return fibonacci(index - 1) + fibonacci(index - 2);
}

console.log(fibonacci(5));