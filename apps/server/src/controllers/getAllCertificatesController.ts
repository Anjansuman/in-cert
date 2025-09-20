import prisma from "@repo/db/client";
import { Request, Response } from "express";


export default async function getAllCertificatesController(req: Request, res: Response) {
    try {

        const certificates = await prisma.certificate.findMany({});

        res.status(200).json({
            success: true,
            message: 'Certificates fetched!',
            certificates: certificates
        });
        return;

    } catch (error) {
        console.error(error);
        res.status(500).json({
            success: false,
            message: 'Internal server error',
        });
        return;
    }
}