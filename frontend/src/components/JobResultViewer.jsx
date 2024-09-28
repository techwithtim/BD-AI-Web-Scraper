import React from 'react';
import { Modal} from 'antd';
import JobResult from './JobResult';


const JobResultViewer = ({ visible, onClose, job }) => {
    if (!job) return null;
    const jobResult = job.result

    return (
        <Modal
            title="Job Result"
            open={visible}
            onCancel={onClose}
            width={800}
            footer={null}
        >
            <JobResult result={jobResult} language={job.scrape_data.language} showBd={false}/>
        </Modal>
    );
};

export default JobResultViewer;