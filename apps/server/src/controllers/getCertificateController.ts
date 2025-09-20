import prisma from "@repo/db/client";
import { Request, Response } from "express";


export default async function getCertificateController(req: Request, res: Response) {
    try {

        const { id } = req.params;

        if(!id) {
            res.status(401).json({
                success: false,
                message: 'Id not found',
            });
            return;
        }

        const certificate = await prisma.certificate.findFirst({
            where: {
                jwt: id,
            },
            select: {
                id: true,
                issuedAt: true,
                candidateId: true,
                candidateName: true,
                description: true,
                uri: true,
                nftHash: true,
                jwt: true,
                verification: true,
                institution: {
                    select: {
                        id: true,
                        name: true,
                    }
                }
            }
        });

        if(!certificate) {
            res.status(404).json({
                success: false,
                message: 'Invalid Id',
            });
            return;
        }

        res.status(200).json({
            success: true,
            message: 'fetched certificate',
            certificate: certificate,
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