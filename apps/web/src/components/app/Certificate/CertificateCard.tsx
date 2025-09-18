import React from "react";

type CertificateCardProps = {
    candidateId: string;
    candidateName: string;
    issuedAt: number; // timestamp (seconds or ms)
    description: string;
    uri?: string;
};

export default function CertificateCard({
    candidateId,
    candidateName,
    issuedAt,
    description,
    uri,
}: CertificateCardProps) {
    // Convert issuedAt to readable date
    const date = new Date(
        issuedAt.toString().length === 10 ? issuedAt * 1000 : issuedAt
    ).toLocaleDateString();

    return (
        <div className="max-w-md w-full bg-neutral-900 text-neutral-100 rounded-2xl shadow-lg p-6 flex flex-col gap-4">
            <h2 className="text-xl font-bold">{candidateName}</h2>

            <div className="text-sm text-neutral-400">
                <p>
                    <span className="font-medium text-neutral-300">ID:</span>{" "}
                    {candidateId}
                </p>
                <p>
                    <span className="font-medium text-neutral-300">Issued:</span> {date}
                </p>
            </div>

            <p className="text-base">{description}</p>

            {uri && (
                <a
                    href={uri}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 text-blue-400 hover:text-blue-300 underline text-sm"
                >
                    View More
                </a>
            )}
        </div>
    );
}
