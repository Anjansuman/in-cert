import prisma from "@repo/db/client";
import { Request, Response } from "express";
import jwt from 'jsonwebtoken';

export default async function createCertificateController(req: Request, res: Response) {
    try {

        // make this feature more secure
        const { institutionId, id, name, description, uri, nftHash } = req.body;

        const issuedAt = new Date();

        const secret = process.env.JWT_SECRET;

        if(!secret) {
            res.status(500).json({
                success: false,
                message: 'Internal server error',
            });
            return;
        }

        const jwtPayload = {
            institutionId: institutionId,
            candidateId: id,
            issuedAt: issuedAt,
            nftHash: nftHash,
        };

        const token = jwt.sign(jwtPayload, secret);

        const certificate = await prisma.certificate.create({
            data: {
                institutionId: institutionId,
                candidateId: id,
                candidateName: name,
                issuedAt: issuedAt,
                description: description,
                uri: uri,
                nftHash: nftHash,
                jwt: token,
            },
        });

        res.status(200).json({
            success: true,
            message: 'Certificate created',
            certificate: certificate,
        });
        return;

    } catch (error) {
        console.error('Error while creating Certificate: ', error);
        res.status(500).json({
            success: false,
            message: 'Internal server error',
        });
        return;
    }
}