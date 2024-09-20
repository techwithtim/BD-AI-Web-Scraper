import React from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import { register } from '../services/api';

const RegisterModal = ({ visible, onCancel, onSwitchToLogin }) => {
    const handleRegister = async (values) => {
        try {
            await register(values.email, values.password);
            message.success('Registration successful. Please log in.');
            onSwitchToLogin();
        } catch (error) {
            message.error('Registration failed. Please try again.');
        }
    };

    return (
        <Modal
            title="Register"
            open={visible}
            onCancel={onCancel}
            footer={null}
        >
            <Form onFinish={handleRegister}>
                <Form.Item name="email" rules={[{ required: true, message: 'Please input your email!' }, { type: 'email', message: 'Please enter a valid email!' }]}>
                    <Input placeholder="Email" />
                </Form.Item>
                <Form.Item name="password" rules={[{ required: true, message: 'Please input your password!' }]}>
                    <Input.Password placeholder="Password" />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit">Register</Button>
                    <Button type="link" onClick={onSwitchToLogin}>
                        Already have an account? Login
                    </Button>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default RegisterModal;