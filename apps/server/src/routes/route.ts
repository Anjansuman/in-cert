import { Router } from "express";
import createInstitutionController from "../controllers/createInstitutionController";
import createCertificateController from "../controllers/createCertificateController";
import getAllCertificatesController from "../controllers/getAllCertificatesController";
import getCertificateController from "../controllers/getCertificateController";

const router: Router = Router();

// router.post('sign-in', );
router.post('/create-institution', createInstitutionController);
router.post('/create-certificate', createCertificateController);

router.get('/get-all-certificates', getAllCertificatesController);
router.get('/get-certificate/:id', getCertificateController);

export default router;