export function parseJsonRejectDuplicateKeys(source) {
  let index = 0;
  const whitespace = () => { while (/\s/.test(source[index] ?? "")) index += 1; };
  const string = () => {
    const start = index;
    if (source[index++] !== '"') throw new SyntaxError("Expected JSON string");
    while (index < source.length) {
      const char = source[index++];
      if (char === '"') return JSON.parse(source.slice(start, index));
      if (char === "\\") index += 1;
      else if (char.charCodeAt(0) < 0x20) throw new SyntaxError("Invalid control character in JSON string");
    }
    throw new SyntaxError("Unterminated JSON string");
  };
  const value = () => {
    whitespace();
    const char = source[index];
    if (char === "{") {
      index += 1; whitespace();
      const keys = new Set();
      if (source[index] === "}") { index += 1; return; }
      while (true) {
        whitespace();
        const key = string();
        if (keys.has(key)) throw new SyntaxError(`Duplicate JSON key: ${key}`);
        keys.add(key); whitespace();
        if (source[index++] !== ":") throw new SyntaxError("Expected colon after JSON object key");
        value(); whitespace();
        const next = source[index++];
        if (next === "}") return;
        if (next !== ",") throw new SyntaxError("Expected comma in JSON object");
      }
    }
    if (char === "[") {
      index += 1; whitespace();
      if (source[index] === "]") { index += 1; return; }
      while (true) {
        value(); whitespace();
        const next = source[index++];
        if (next === "]") return;
        if (next !== ",") throw new SyntaxError("Expected comma in JSON array");
      }
    }
    if (char === '"') { string(); return; }
    const match = /^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/.exec(source.slice(index));
    if (!match) throw new SyntaxError("Invalid JSON value");
    index += match[0].length;
  };
  value(); whitespace();
  if (index !== source.length) throw new SyntaxError("Trailing content after JSON value");
  return JSON.parse(source);
}
