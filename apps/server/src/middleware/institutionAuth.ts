import { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";


export default function institutionAuth(req: Request, res: Response, next: NextFunction) {
    try {
        
        const authToken = req.headers.authorization;

        if(!authToken || !authToken.startsWith('Bearer')) {
            res.status(404).json({
                success: false,
                message: 'Invalid auth token!',
            });
            return;
        }

        const token = authToken.split(' ')[1];
        const secret = process.env.JWT_SECRET;

        if(!token) {
            res.status(404).json({
                success: false,
                message: 'Token not found',
            });
            return;
        }

        if(!secret) {
            res.status(500).json({
                success: false,
                message: 'Internal server error',
            });
            return;
        }

        const verifiedToken = jwt.verify(token, secret, (err, decoded) => {
            if(err) {
                res.status(401).json({
                    success: false,
                    message: 'Not authorised',
                });
                return;
            }
            req.institution = decoded as AuthInstitute;
            next();
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            success: false,
            message: 'Internal server error',
        });
        return;
    }
}