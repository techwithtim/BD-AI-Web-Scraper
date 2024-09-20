import React, { useState, useEffect } from 'react';
import { Table, Tag, Button, message } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import { getUserJobs, deleteJob } from '../services/api';

const UserJobs = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchJobs();
    }, []);

    const fetchJobs = async () => {
        try {
            const fetchedJobs = await getUserJobs();
            setJobs(fetchedJobs);
        } catch (error) {
            console.error("Failed to fetch jobs:", error);
            message.error("Failed to fetch jobs");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (jobId) => {
        try {
            await deleteJob(jobId);
            message.success("Job deleted successfully");
            fetchJobs();  // Refresh the job list
        } catch (error) {
            console.error("Failed to delete job:", error);
            message.error("Failed to delete job");
        }
    };

    const columns = [
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            render: status => (
                <Tag color={status === 'COMPLETED' ? 'green' : status === 'FAILED' ? 'red' : 'blue'}>
                    {status}
                </Tag>
            ),
        },
        {
            title: 'Start Time',
            dataIndex: 'start_time',
            key: 'start_time',
            render: time => new Date(time).toLocaleString(),
        },
        {
            title: 'End Time',
            dataIndex: 'end_time',
            key: 'end_time',
            render: time => time ? new Date(time).toLocaleString() : 'N/A',
        },
        {
            title: 'URL',
            dataIndex: ['scrape_data', 'url'],
            key: 'url',
        },
        {
            title: 'Action',
            dataIndex: "_id",
            key: 'action',
            render: _id => (
                <Button
                    type="danger"
                    icon={<DeleteOutlined />}
                    onClick={() => handleDelete(_id)}
                >
                    Delete
                </Button>
            ),
        },
    ];

    return (
        <Table
            dataSource={jobs}
            columns={columns}
            rowKey="id"
            loading={loading}
        />
    );
};

export default UserJobs;