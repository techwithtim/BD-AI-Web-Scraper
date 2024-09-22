import React, { useState } from 'react';
import { Form, Input, Select, Slider, Button, message } from 'antd';
import IFrameWebsitePreview from "./IFramePreview"
import { useAuth } from '../contexts/AuthContext';
import { ActionTypes } from "../enums/actions"
import JobHandler from "./JobHandler"

const { Option } = Select;
const { TextArea } = Input;

const ScrapeForm = ({ showLogin }) => {
    const { isLoggedIn } = useAuth();
    const [showPreview, setShowPreview] = useState(false)
    const [scrapeData, setScrapeData] = useState({
        url: '',
        language: 'python',
        library: 'selenium',
        prompt: '',
        performace: 1
    });

    const handleInputChange = (name, value) => {
        setScrapeData({ ...scrapeData, [name]: value });
    };

    const handleAction = (action) => {

        if (!isLoggedIn) {
            showLogin()
            return
        }

        switch (action) {
            case ActionTypes.SHOW_PREVIEW:
                if (scrapeData.url)
                    setShowPreview(true);
                else
                    message.error("Please enter a valid URL.")
                break;
            default:
                console.log('Unknown action:', action);
        }
    };


    return (
        <Form layout="vertical" style={{ marginTop: '20px' }}>
            <Form.Item label="Website">
                <Input
                    value={scrapeData.url}
                    onChange={(e) => handleInputChange('url', e.target.value)}
                    placeholder="Enter website URL"
                />
            </Form.Item>
            <Form.Item>
                <Button onClick={() => handleAction(ActionTypes.SHOW_PREVIEW)}>Show Preview</Button>
            </Form.Item>
            {showPreview && <IFrameWebsitePreview url={scrapeData.url} />}
            <Form.Item label="Language">
                <Select
                    value={scrapeData.language}
                    onChange={(value) => handleInputChange('language', value)}
                >
                    <Option value="python">Python</Option>
                    <Option value="javascript">JavaScript</Option>
                </Select>
            </Form.Item>
            <Form.Item label="Library">
                <Select
                    value={scrapeData.library}
                    onChange={(value) => handleInputChange('library', value)}
                >
                    <Option value="selenium">Selenium</Option>
                    <Option value="playwright">Playwright</Option>
                    <Option value="puppeteer">Puppeteer</Option>
                </Select>
            </Form.Item>
            <Form.Item label="Prompt">
                <TextArea
                    value={scrapeData.prompt}
                    onChange={(e) => handleInputChange('prompt', e.target.value)}
                    rows={4}
                />
            </Form.Item>
            <Form.Item label="Performance">
                <Slider
                    min={1}
                    max={4}
                    value={scrapeData.performance}
                    onChange={(value) => handleInputChange('performance', value)}
                />
            </Form.Item>
            {isLoggedIn ? (
                <JobHandler scrapeData={scrapeData} />
            ) : (
                <p>Please log in to generate scraping code.</p>
            )}
        </Form>
    );
};

export default ScrapeForm;