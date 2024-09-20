import React, { useState } from 'react';

const IFrameWebsitePreview = ({ url }) => {
    const [loading, setLoading] = useState(true);

    return (
        <div className="website-preview" style={{ width: '100%', maxWidth: '600px', height: '400px', border: '1px solid #ccc', borderRadius: '8px', overflow: 'hidden' }}>
            {loading && <div style={{ padding: '10px' }}>Loading preview...</div>}
            <iframe
                src={url}
                title="Website Preview"
                width="100%"
                height="100%"
                style={{ border: 'none' }}
                onLoad={() => setLoading(false)}
            />
        </div>
    );
};

export default IFrameWebsitePreview;