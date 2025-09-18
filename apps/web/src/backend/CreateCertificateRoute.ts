import axios from 'axios';
import { CREATE_CERTIFICATE_URL } from './route';

export default async function createCertificateRoute(
    institutionId: string,
    candidateId: string,
    candidateName: string,
    issuedAt: number,
    description: string,
    uri?: string,
) {
    try {
        
        const data = await axios.post(
            CREATE_CERTIFICATE_URL,
            {
                institutionId,
                id: candidateId,
                name: candidateName,
                issuedAt,
                description,
                uri,
            }
        );

        return data;

    } catch (error) {
        console.error(error);
    }
}