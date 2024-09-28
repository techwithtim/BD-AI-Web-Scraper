import React from "react";
import { Typography, Steps, Card } from "antd";
import { CodeOutlined, ChromeOutlined, LinkOutlined } from "@ant-design/icons";
import CodeDisplay from "./CodeDisplay";

const { Title, Paragraph, Link } = Typography;
const { Step } = Steps;

const SetupInstructions = ({ instructions }) => {
  const parseInstructions = (text) => {
    const steps = text.split(/\d+\./).filter((step) => step.trim() !== "");
    return steps.map((step, index) => {
      const lines = step.trim().split("\n");
      const title = lines[0];
      const content = lines.slice(1).join("\n");

      let icon;
      if (title.toLowerCase().includes("install")) {
        icon = <CodeOutlined />;
      } else if (title.toLowerCase().includes("download")) {
        icon = <ChromeOutlined />;
      } else {
        icon = <LinkOutlined />;
      }

      return {
        title,
        content,
        icon,
      };
    });
  };

  const renderContent = (content) => {
    const parts = content.split("```");
    return parts.map((part, index) => {
      if (index % 2 === 1) {
        // This is a code block
        const [language, ...code] = part.split("\n");
        while (code[code.length - 1].trim() === "") code.pop();

        return (
          <CodeDisplay
            key={index}
            code={code.join("\n")}
            language={language.trim()}
          />
        );
      } else {
        // This is regular text
        return (
          <Paragraph key={index}>
            {part.split("\n").map((line, lineIndex) => {
              if (line.startsWith("- [")) {
                const [_, text, url] = line.match(/- \[(.*?)\]\((.*?)\)/);
                return (
                  <div key={lineIndex}>
                    <Link href={url} target="_blank">
                      {text}
                    </Link>
                  </div>
                );
              } else {
                return <div key={lineIndex}>{line}</div>;
              }
            })}
          </Paragraph>
        );
      }
    });
  };

  const parsedSteps = parseInstructions(instructions);

  return (
    <Card
      title={<Title level={4}>Setup Instructions</Title>}
      style={{ marginBottom: 16 }}
    >
      <Steps direction="vertical">
        {parsedSteps.map((step, index) => (
          <Step
            key={index}
            title={step.title}
            status="process"
            description={renderContent(step.content)}
            icon={step.icon}
          />
        ))}
      </Steps>
    </Card>
  );
};

export default SetupInstructions;
