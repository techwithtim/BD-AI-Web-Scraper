import React from 'react';
import { Typography, Card } from 'antd';
import ReactHtmlParser from 'react-html-parser';
import CodeDisplay from './CodeDisplay';
import SetupInstructions from './SetupInstructions';

const { Paragraph } = Typography;

const JobResult = ({ result, language }) => {
    if (!result) return null;

    return (
        <div>
            {result.html && (
                <Card title="Website Preview" style={{ marginBottom: 16 }}>
                    <div style={{ height: 500, overflow: 'auto' }}>
                        {ReactHtmlParser(result.html)}
                    </div>
                </Card>
            )}

            {result.tags && Object.keys(result.tags).length === 0 && result.text && (
                <Paragraph>{result.text}</Paragraph>
            )}

            {result.tags && Object.entries(result.tags).map(([key, content]) => {
                if (key === "SCRAPING_CODE") {
                    return (
                        <Card title="Generated Code" key={key} style={{ marginBottom: 16 }}>
                            <CodeDisplay code={content} language={language.toLowerCase()} />
                        </Card>
                    );
                } else if (key === "SETUP_INSTRUCTIONS") {
                    return <SetupInstructions key={key} instructions={content} />;
                } else {
                    return (
                        <Card title={key} key={key} style={{ marginBottom: 16 }}>
                            <Paragraph>{content}</Paragraph>
                        </Card>
                    );
                }
            })}
        </div>
    );
};

export default JobResult;