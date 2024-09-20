import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const CodeDisplay = ({ code, language }) => {
    // Remove any lines that contain ```
    const trimmedCode = code
        .split('\n')
        .filter(line => !line.includes('```'))
        .join('\n');

    // If language is included in the first line, extract it
    const lines = trimmedCode.split('\n');
    let codeLanguage = language;
    let codeContent = trimmedCode;

    if (lines[0].trim().match(/^[a-zA-Z]+$/)) {
        codeLanguage = lines[0].trim();
        codeContent = lines.slice(1).join('\n');
    }

    return (
        <SyntaxHighlighter
            language={codeLanguage.toLowerCase()}
            style={vscDarkPlus}
            showLineNumbers={true}
            wrapLines={true}
        >
            {codeContent}
        </SyntaxHighlighter>
    );
};

export default CodeDisplay;