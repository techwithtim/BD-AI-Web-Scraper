import React, { useState, useEffect } from "react";
import { Table, Tag, Button, message } from "antd";
import { DeleteOutlined, EyeOutlined } from "@ant-design/icons";
import { getUserJobs, deleteJob } from "../services/api";
import JobResultViewer from "./JobResultViewer";
import { ScraperStatus } from "../enums/status";

const UserJobs = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedJob, setSelectedJob] = useState(null);
    const [resultViewerVisible, setResultViewerVisible] = useState(false);

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
            fetchJobs(); // Refresh the job list
        } catch (error) {
            console.error("Failed to delete job:", error);
            message.error("Failed to delete job");
        }
    };

    const handleViewResult = (job) => {
        setSelectedJob(job);
        setResultViewerVisible(true);
    };

    const columns = [
        {
            title: "Status",
            dataIndex: "status",
            key: "status",
            render: (status) => (
                <Tag
                    color={
                        status === ScraperStatus.COMPLETED
                            ? "green"
                            : status === ScraperStatus.FAILED
                                ? "red"
                                : "blue"
                    }
                >
                    {status}
                </Tag>
            ),
        },
        {
            title: "Start Time",
            dataIndex: "start_time",
            key: "start_time",
            render: (time) => new Date(time).toLocaleString(),
        },
        {
            title: "End Time",
            dataIndex: "end_time",
            key: "end_time",
            render: (time) => (time ? new Date(time).toLocaleString() : "N/A"),
        },
        {
            title: "URL",
            dataIndex: ["scrape_data", "url"],
            key: "url",
        },
        {
            title: "Action",
            key: "action",
            render: (_, record) => (
                <>
                    <Button
                        type="primary"
                        icon={<EyeOutlined />}
                        onClick={() => handleViewResult(record)}
                        style={{ marginRight: 8 }}
                        disabled={record.status !== ScraperStatus.COMPLETED}
                    >
                        View Result
                    </Button>
                    <Button
                        type="danger"
                        icon={<DeleteOutlined />}
                        onClick={() => handleDelete(record._id)}
                    >
                        Delete
                    </Button>
                </>
            ),
        },
    ];

    return (
        <>
            <Table
                dataSource={jobs}
                columns={columns}
                rowKey="id"
                loading={loading}
            />
            <JobResultViewer
                visible={resultViewerVisible}
                onClose={() => setResultViewerVisible(false)}
                job={selectedJob}
            />
        </>
    );
};

export default UserJobs;
