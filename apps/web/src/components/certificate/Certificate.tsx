"use client";

import axios from "axios";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import QRCodeLib from "qrcode";
import { FiCopy, FiExternalLink } from "react-icons/fi";
import Ribbon from "../ui/Ribbon";

export default function Certificate() {
    const [certificateData, setCertificateData] = useState<any>();
    const [qrDataUrl, setQrDataUrl] = useState<string | null>(null);
    const searchParams = useSearchParams();
    const id = searchParams.get("id");

    async function fetchData() {
        if (!id) return;

        const { data } = await axios.get(
            `http://localhost:8080/api/v1/get-certificate/${id}`
        );

        setCertificateData(data.certificate);

        const qrUrl = await QRCodeLib.toDataURL(data.certificate.jwt, {
            errorCorrectionLevel: "H",
            color: {
                dark: "#000000",
                light: "#ffffff",
            },
        });
        setQrDataUrl(qrUrl);
    }

    useEffect(() => {
        fetchData();
    }, []);

    if (!certificateData) {
        return (
            <div className="h-[700px] w-full flex items-center justify-center bg-gray-100 text-gray-800 rounded-lg border border-gray-300 shadow-md">
                Loading Certificate...
            </div>
        );
    }

    const explorerUrl = `https://explorer.solana.com/tx/${certificateData.nftHash}?cluster=devnet`;

    const copyToClipboard = async (text: string) => {
        await navigator.clipboard.writeText(text);
    };

    return (
        <div className="h-[750px] w-full bg-gradient-to-br from-white to-gray-100 rounded-xl border-2 border-teal-950 shadow-lg p-10 flex flex-col items-center justify-between text-gray-800 relative">
            <div className="absolute top-0 left-10">
                <Ribbon />
            </div>
            <div className="text-center">
                <h1 className="text-4xl font-extrabold text-teal-950 tracking-widest">
                    Certificate of Achievement
                </h1>
                <p className="mt-2 text-lg text-gray-600">
                    Awarded by{" "}
                    <span className="font-semibold text-teal-900 ">
                        {certificateData.institution.name}
                    </span>
                </p>
            </div>

            <div className="flex flex-col items-center text-center">
                <p className="text-gray-600 text-lg">This is to certify that</p>
                <h2 className="text-3xl font-bold mt-3 text-gray-800 underline decoration-teal-900">
                    {certificateData.candidateName}
                </h2>
                <p className="mt-4 text-gray-600 max-w-xl">
                    {certificateData.description}
                </p>
            </div>

            <div className="w-full flex justify-between items-end mt-8">
                <div className="flex flex-col items-start gap-y-2 ">
                    <div className="">
                        {qrDataUrl ? (
                            <img
                                src={qrDataUrl}
                                alt="JWT QR Code"
                                width={120}
                                height={120}
                                className="bg-neutral-600 p-0.5 rounded"
                            />
                        ) : (
                            <p className="text-sm text-neutral-500">Generating QR...</p>
                        )}
                    </div>
                    <p className="text-sm text-gray-600">
                        Issued At:{" "}
                        <span className="text-gray-800">
                            {new Date(certificateData.issuedAt).toDateString()}
                        </span>
                    </p>
                    <p className="text-sm text-gray-600">
                        Certificate ID:{" "}
                        <span className="text-gray-800">{certificateData.id}</span>
                    </p>
                </div>

                <div className="text-right">
                    <p className="text-sm text-gray-600">
                        Verification Status:{" "}
                        <span
                            className={`${certificateData.verification === "VERIFIED"
                                ? "text-green-500"
                                : "text-red-500"
                                } font-semibold`}
                        >
                            {certificateData.verification}
                        </span>
                    </p>

                    <div className="flex items-center gap-2 mt-2 text-xs">
                        <span className="truncate max-w-[180px]">{certificateData.nftHash}</span>
                        <button
                            onClick={() => copyToClipboard(certificateData.nftHash)}
                            className="text-yellow-500 hover:text-yellow-600"
                            title="Copy NFT Hash"
                        >
                            <FiCopy size={14} />
                        </button>
                        <a
                            href={explorerUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 hover:text-blue-600"
                            title="View on Solana Explorer"
                        >
                            <FiExternalLink size={14} />
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}
