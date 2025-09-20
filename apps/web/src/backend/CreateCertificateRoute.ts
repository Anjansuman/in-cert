import axios from 'axios';
import { API_URL, BACKEND_URL, CREATE_CERTIFICATE_URL } from './route';

export default async function createCertificateRoute(
    institutionId: string,
    candidateId: string,
    candidateName: string,
    issuedAt: number,
    description: string,
    nftHash: string,
    uri?: string,
) {
    try {

        console.log({ BACKEND_URL });
        console.log({ API_URL });
        
        console.log("route: ", CREATE_CERTIFICATE_URL);
        const data = await axios.post(
            'http://localhost:8080/api/v1/create-certificate',
            {
                institutionId,
                id: candidateId,
                name: candidateName,
                issuedAt,
                description,
                uri,
                nftHash,
            }
        );

        return data;

    } catch (error) {
        console.error(error);
    }
}