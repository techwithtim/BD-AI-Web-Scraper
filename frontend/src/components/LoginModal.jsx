import React from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import { useAuth } from '../contexts/AuthContext';

const LoginModal = ({ visible, onCancel, onSwitchToRegister }) => {
    const { login } = useAuth();

    const handleLogin = async (values) => {
        try {
            await login(values.username, values.password);
            message.success('Login successful');
            onCancel();
        } catch (error) {
            message.error('Login failed. Please check your credentials.');
        }
    };

    return (
        <Modal
            title="Login"
            open={visible}
            onCancel={onCancel}
            footer={null}
        >
            <Form onFinish={handleLogin}>
                <Form.Item name="username" rules={[{ required: true, message: 'Please input your email!' }]}>
                    <Input placeholder="Email" />
                </Form.Item>
                <Form.Item name="password" rules={[{ required: true, message: 'Please input your password!' }]}>
                    <Input.Password placeholder="Password" />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit">Login</Button>
                    <Button type="link" onClick={onSwitchToRegister}>
                        Don't have an account? Register
                    </Button>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default LoginModal;