import React from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

const CodeDisplay = ({ code, language, className }) => {
  let codeContent;
  try {
    // Remove any lines that contain ```
    const trimmedCode = code
      .split("\n")
      .filter((line) => !line.includes("```"))
      .join("\n");

    // If language is included in the first line, extract it
    const lines = trimmedCode.slice(1, trimmedCode.length - 1);
    codeContent = lines;

    if (lines[0].trim().match(/^[a-zA-Z]+$/)) {
      codeContent = lines.slice(1).join("\n");
    }
  } catch {
    codeContent = code;
  }

  return (
    <div style={{ width: "100%", maxWidth: "100%" }} className={className}>
      <SyntaxHighlighter
        language={language.toLowerCase()}
        style={{ ...vscDarkPlus, width: 100 }}
        showLineNumbers={true}
        wrapLines={true}
      >
        {codeContent}
      </SyntaxHighlighter>
    </div>
  );
};

export default CodeDisplay;
