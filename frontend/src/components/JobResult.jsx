import React, { useState, useEffect } from "react";
import { Typography, Card, Button } from "antd";
import ReactHtmlParser from "react-html-parser";
import CodeDisplay from "./CodeDisplay";
import SetupInstructions from "./SetupInstructions";
import BdAd from "./BdAd";
import "../css/JobResult.css";

const { Paragraph } = Typography;

const JobResult = ({ result, language, showBd=true }) => {
  if (!result) return null;

  const [loading, setLoading] = useState(true);
  const [code, setCode] = useState("");
  const [preview, setPreview] = useState("No preview");
  const [instructions, setInstructions] = useState("");
  const [text, setText] = useState("");
  const [showCode, setShowCode] = useState(true);

  useEffect(() => {
    parseResults();
  }, [result]);

  const parseResults = () => {
    setLoading(true);
    if (result.html) setPreview(result.html);

    Object.entries(result.tags).map(([key, content]) => {
      if (key === "SCRAPING_CODE") {
        setCode(content);
      } else if (key === "SETUP_INSTRUCTIONS") {
        setInstructions(content);
      } else {
        setText("");
      }
    });

    setLoading(false);
  };

  if (loading) return <></>;

  const header = (
    <div className="result-header">
      <h4>Result</h4>
      <Button onClick={() => setShowCode(!showCode)}>
        {!showCode ? "View Code" : "Show Preview"}
      </Button>
    </div>
  );

  return (
    <div className="result">
      {result.tags && Object.keys(result.tags).length === 0 && result.text && (
        <Paragraph>{result.text}</Paragraph>
      )}
      <Card title={header} style={{marginBottom: 10}}>
        {showCode ? <CodeDisplay
          code={code}
          language={language.toLowerCase()}
          className="item"
        /> : <div className="html-display">{ReactHtmlParser(preview)}</div>}
      </Card>

      {instructions && <SetupInstructions instructions={instructions} />}
      {text && (
        <Card>
          <Paragraph>{text}</Paragraph>
        </Card>
      )}
      {showBd && <BdAd />}
    </div>
  );
};

export default JobResult;
