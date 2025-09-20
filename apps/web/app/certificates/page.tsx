"use client";
import { useEffect, useState } from "react";
import CertificateCard from "@/src/components/app/Certificate/CertificateCard";
import axios from "axios";


export default function Certificates() {

    const [certificates, setCertificates] = useState<any[]>();

    async function get() {
        const response = await axios.get(
            'http://localhost:8080/api/v1/get-all-certificates',
        );
        const data = await response.data;
        setCertificates(data.certificates);
    }

    useEffect(() => {
        get();
    }, [])

    return (
        <div className="w-full h-full px-20 py-30 bg-neutral-800 flex justify-center ">
            <div className="flex gap-6 justify-start flex-wrap ">
                {certificates?.map((c, index) => (
                    <CertificateCard
                        key={index}
                        id={c.id}
                        institutionId={c.institutionId}
                        candidateId={c.candidateId}
                        candidateName={c.candidateName}
                        issuedAt={c.issuedAt}
                        description={c.description}
                        uri={c.uri}
                        nftHash={c.nftHash}
                        jwt={c.jwt}
                    />
                ))}
            </div>
        </div>
    );
}