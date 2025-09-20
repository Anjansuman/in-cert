import { Request, Response } from "express";
import multer from "multer";
import FormData from "form-data";
import axios from "axios";
import jwt from "jsonwebtoken";

// Use memory storage for temporary testing - no files saved to disk
const storage = multer.memoryStorage();

const fileFilter = (req: any, file: Express.Multer.File, cb: multer.FileFilterCallback) => {
    // Accept only PDF and image files
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'application/pdf'];

    if (allowedTypes.includes(file.mimetype)) {
        cb(null, true);
    } else {
        cb(new Error('Invalid file type. Only PDF and image files are allowed.'));
    }
};

const upload = multer({
    storage,
    fileFilter,
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB limit
    }
});

// Middleware to handle single file upload
export const uploadMiddleware = upload.single('certificate');

export default async function verifyCertificateController(req: Request, res: Response) {
    try {
        // Check if file was uploaded
        if (!req.file) {
            res.status(400).json({
                success: false,
                message: 'No file uploaded. Please provide a certificate file (PDF or image).',
            });
            return;
        }

        console.log('File received for testing:', {
            originalName: req.file.originalname,
            mimetype: req.file.mimetype,
            size: req.file.size,
            buffer: req.file.buffer ? 'Buffer present' : 'No buffer'
        });

        // Prepare form data for Python service using buffer (no file saved to disk)
        const formData = new FormData();
        formData.append('file', req.file.buffer, {
            filename: req.file.originalname,
            contentType: req.file.mimetype
        });

        // Send file to Python extraction service
        console.log('Sending file to Python extraction service...');

        const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:5000/extract-data';

        const pythonResponse = await axios.post(pythonServiceUrl, formData, {
            headers: {
                ...formData.getHeaders(),
                'Content-Type': 'multipart/form-data',
            },
            timeout: 30000, // 30 second timeout
        });

        console.log('Python service response:', pythonResponse.data);

        // Extract name and URL from Python response
        const { name, token } = pythonResponse.data;

        if (!name || !token) {
            console.log('Incomplete data from Python service:', { name, token });
            res.status(422).json({
                success: false,
                message: 'Could not extract complete certificate data. Name or token missing.',
                extractedData: { name, token }
            });
            return;
        }

        const secret = process.env.JWT_SECRET;

        if (!secret) throw new Error('jwt secret not found');

        let payload;

        const isVerified = jwt.verify(token, secret, (err: any, decoded: any) => {
            if (err) {
                res.status(400).json({
                    success: false,
                    message: "certificate is forged",
                });
                return;
            } else {
                payload = decoded;
            }
        });

        // Log the extracted data for testing
        console.log('Extracted certificate data: ', {
            name,
            token,
            originalFile: req.file.originalname,
            fileSize: req.file.size,
            timestamp: new Date().toISOString(),
        });

        // in here the file will be deleted after verification

        res.status(200).json({
            success: true,
            message: 'Certificate data extracted successfully (test mode)',
            data: {
                name,
                token,
                extractedAt: new Date().toISOString(),
                testInfo: {
                    fileName: req.file.originalname,
                    fileSize: req.file.size,
                    autoDeleted: true
                }
            }
        });
        return;

    } catch (error: any) {
        console.error(error);

        if (error.code === 'ECONNREFUSED') {
            res.status(503).json({
                success: false,
                message: 'Python extraction service is unavailable. Please try again later.',
            });
            return;
        }

        if (error.response?.status === 400) {
            res.status(400).json({
                success: false,
                message: 'Invalid file format or corrupted file.',
                error: error.response.data?.message || 'Python service rejected the file'
            });
            return;
        }

        if (error.code === 'ETIMEDOUT') {
            res.status(408).json({
                success: false,
                message: 'File processing timeout. Please try with a smaller file.',
            });
            return;
        }

        res.status(500).json({
            success: false,
            message: 'Internal server error during certificate verification test',
            error: process.env.NODE_ENV === 'development' ? error.message : undefined
        });
        return;
    }
}