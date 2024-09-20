import React from 'react';
import { Modal, Typography, Card } from 'antd';
import ReactHtmlParser from 'react-html-parser';
import CodeDisplay from './CodeDisplay';

const { Paragraph } = Typography;

const JobResultViewer = ({ visible, onClose, job }) => {
    if (!job) return null;
    console.log(job)
    const jobResult = job.result

    return (
        <Modal
            title="Job Result"
            open={visible}
            onCancel={onClose}
            width={800}
            footer={null}
        >
            {jobResult.html && (
                <Card title="Website Preview" style={{ marginBottom: 16 }}>
                    <div style={{ height: 300, overflow: 'auto' }}>
                        {ReactHtmlParser(jobResult.html)}
                    </div>
                </Card>
            )}

            {jobResult.tags && Object.entries(jobResult.tags).map(([key, content]) => {
                if (key === "SCRAPING_CODE") {
                    return (
                        <Card title="Generated Code" key={key} style={{ marginBottom: 16 }}>
                            <CodeDisplay code={content} language={job.scrape_data.language.toLowerCase()} />
                        </Card>
                    );
                } else {
                    return (
                        <Card title={key} key={key} style={{ marginBottom: 16 }}>
                            <Paragraph>{content}</Paragraph>
                        </Card>
                    );
                }
            })}
        </Modal>
    );
};

export default JobResultViewer;