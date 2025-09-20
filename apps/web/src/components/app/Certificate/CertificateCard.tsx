"use client";

import React, { useEffect, useState } from "react";
import QRCodeLib from "qrcode";
import { HiOutlineClipboard, HiCheck } from "react-icons/hi";

type CertificateCardProps = {
    id: string;
    institutionId: string;
    candidateId: string;
    candidateName: string;
    issuedAt: string | Date;
    description: string;
    uri?: string;
    nftHash: string;
    jwt: string;
};

export default function CertificateCard({
    id,
    institutionId,
    candidateId,
    candidateName,
    issuedAt,
    description,
    uri,
    nftHash,
    jwt,
}: CertificateCardProps) {
    const [qrDataUrl, setQrDataUrl] = useState<string | null>(null);
    const [copied, setCopied] = useState(false);

    const certificateUrl = `http://localhost:3000/certificate/?id=${encodeURIComponent(jwt)}`;

    useEffect(() => {
        let mounted = true;

        QRCodeLib.toDataURL(certificateUrl, { errorCorrectionLevel: "M" })
            .then((dataUrl) => {
                if (mounted) setQrDataUrl(dataUrl);
            })
            .catch((err) => {
                console.error("QR generation error:", err);
            });

        return () => {
            mounted = false;
        };
    }, [certificateUrl]);

    const date = new Date(issuedAt).toLocaleDateString();

    const handleCopyNft = async () => {
        await navigator.clipboard.writeText(nftHash);
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
    };

    const truncate = (str: string, front = 6, back = 4) =>
        str.length > front + back
            ? `${str.slice(0, front)}...${str.slice(-back)}`
            : str;

    return (
        <div className="max-w-md w-full h-fit bg-neutral-900 text-neutral-100 rounded-2xl shadow-lg p-6 flex flex-col gap-4">
            <h2 className="text-xl font-bold">{candidateName}</h2>

            <div className="text-sm text-neutral-400 space-y-1">
                <p>
                    <span className="font-medium text-neutral-300">Certificate ID:</span>{" "}
                    {id}
                </p>
                <p>
                    <span className="font-medium text-neutral-300">Institution ID:</span>{" "}
                    {institutionId}
                </p>
                <p>
                    <span className="font-medium text-neutral-300">Candidate ID:</span>{" "}
                    {candidateId}
                </p>
                <p>
                    <span className="font-medium text-neutral-300">Issued:</span> {date}
                </p>
                <p className="flex items-center gap-2">
                    <span className="font-medium text-neutral-300">NFT Hash:</span>{" "}
                    <span className="font-mono">{truncate(nftHash)}</span>
                    <button
                        onClick={handleCopyNft}
                        className="text-neutral-400 hover:text-neutral-200 transition"
                        title="Copy NFT Hash"
                    >
                        {copied ? (
                            <HiCheck className="w-4 h-4 text-green-400" />
                        ) : (
                            <HiOutlineClipboard className="w-4 h-4" />
                        )}
                    </button>
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

            <div className="mt-4 flex flex-col items-center">
                <span className="text-sm text-neutral-400 mb-2">Certificate QR</span>

                {qrDataUrl ? (
                    <>
                        <a href={certificateUrl} target="_blank" rel="noopener noreferrer">
                            <img
                                src={qrDataUrl}
                                alt="JWT QR Code"
                                width={160}
                                height={160}
                                className="bg-white p-1 rounded hover:scale-105 transition"
                            />
                        </a>

                        <div className="mt-3 flex gap-2">
                            <a
                                href={certificateUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="px-3 py-1 bg-green-600 rounded text-white text-sm"
                            >
                                Open Certificate
                            </a>
                            <button
                                onClick={() => navigator.clipboard.writeText(jwt)}
                                className="px-3 py-1 bg-zinc-800 rounded text-white text-sm"
                            >
                                Copy JWT
                            </button>
                        </div>
                    </>
                ) : (
                    <p className="text-sm text-neutral-500">Generating QR...</p>
                )}
            </div>
        </div>
    );
}
