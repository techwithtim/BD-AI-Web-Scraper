import React, { useState, useEffect } from 'react';
import { Tag, Tooltip } from 'antd';
import { ClockCircleOutlined } from '@ant-design/icons';
import { ScraperStatus } from '../enums/status';

const statusColors = {
    [ScraperStatus.STARTED]: 'blue',
    [ScraperStatus.IN_PROGRESS]: 'orange',
    [ScraperStatus.COMPLETED]: 'green',
    [ScraperStatus.FAILED]: 'red',
    [ScraperStatus.CANCELLED]: 'default'
};

const JobStatusDisplay = ({ status, startTime }) => {
    const [elapsedTime, setElapsedTime] = useState(0);

    useEffect(() => {
        let timer;
        if (status === ScraperStatus.STARTED || status === ScraperStatus.IN_PROGRESS) {
            timer = setInterval(() => {
                const now = new Date();
                const elapsed = Math.floor((now - new Date(startTime)) / 1000); // elapsed time in seconds
                setElapsedTime(elapsed);
            }, 1000);
        } else {
            // Calculate final elapsed time when job is completed, failed, or cancelled
            const endTime = new Date();
            const finalElapsed = Math.floor((endTime - new Date(startTime)) / 1000);
            setElapsedTime(finalElapsed);
        }

        return () => {
            if (timer) clearInterval(timer);
        };
    }, [startTime, status]);

    const formatElapsedTime = (seconds) => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const remainingSeconds = seconds % 60;

        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    };

    return (
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px', marginBottom: 10 }}>
            <Tag color={statusColors[status]}>{status}</Tag>
            <Tooltip title="Elapsed Time">
                <Tag icon={<ClockCircleOutlined />} color="default">
                    {formatElapsedTime(elapsedTime)}
                </Tag>
            </Tooltip>
        </div>
    );
};

export default JobStatusDisplay;