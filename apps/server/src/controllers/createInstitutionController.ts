import prisma from "@repo/db/client";
import { Request, Response } from "express";


export default async function createInstitutionController(req: Request, res: Response) {
    try {
        
        const { name } = req.body;

        if(!name || typeof name !== 'string') {
            res.status(401).json({
                success: false,
                message: "Invalid name or it's format",
            });
            return;
        }

        const existingInstitution = await prisma.institution.findUnique({
            where: {
                name: name,
            },
        });

        if(existingInstitution) {
            res.status(402).json({
                success: false,
                message: "Institute with this name already exist.",
            });
            return;
        }

        const institution = await prisma.institution.create({
            data: {
                name: name,
            },
            select: {
                id: true,
                name: true,
                verification: true,
            }
        });

        res.status(201).json({
            success: true,
            message: 'Institution created successfully!',
            institution: institution,
        });
        return;

    } catch (error) {
        console.error('Error while creating Institution: ', error);
        res.status(500).json({
            success: false,
            message: 'Internal server error',
        });
        return;
    }
}