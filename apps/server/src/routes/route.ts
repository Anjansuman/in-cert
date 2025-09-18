import { Router } from "express";
import createInstitutionController from "../controllers/createInstitutionController";

const router: Router = Router();

// router.post('sign-in', );
router.post('/create-institution', createInstitutionController);

export default router;