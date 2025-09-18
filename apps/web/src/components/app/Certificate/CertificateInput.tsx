"use client";

import { useContract } from "@/app/contract";
import createCertificateRoute from "@/src/backend/CreateCertificateRoute";
import React, { useState } from "react";

export default function CertificateForm() {
    const [candidateId, setCandidateId] = useState("");
    const [candidateName, setCandidateName] = useState("");
    const [issuedAt, setIssuedAt] = useState<number>(0);
    const [description, setDescription] = useState("");
    const [uri, setUri] = useState("");
    const { contract } = useContract();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!contract) return;

        const res = await contract.createCertificate(
            'cmfogpipy0000lph074hfu3xl',
            'institute_1',
            candidateId,
            candidateName,
            issuedAt,
            description,
            uri,
        );

        console.log('solana data: ', res);

        const data = await createCertificateRoute(
            'cmfogpipy0000lph074hfu3xl',
            candidateId,
            candidateName,
            issuedAt,
            description,
            uri,
        );

        console.log('backend data: ', data);

        setCandidateId("");
        setCandidateName("");
        setIssuedAt(0);
        setDescription("");
        setUri("");
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="max-w-md w-full bg-black text-gray-100 p-6 rounded-2xl shadow-lg flex flex-col gap-4"
        >
            <h2 className="text-xl font-bold mb-2 text-white">Create Certificate</h2>

            <input
                type="text"
                placeholder="Candidate ID"
                value={candidateId}
                onChange={(e) => setCandidateId(e.target.value)}
                className="p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
            />

            <input
                type="text"
                placeholder="Candidate Name"
                value={candidateName}
                onChange={(e) => setCandidateName(e.target.value)}
                className="p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
            />

            <input
                type="date"
                value={issuedAt ? new Date(issuedAt).toISOString().split("T")[0] : ""}
                onChange={(e) => {
                    const timestamp = new Date(e.target.value).getTime();
                    setIssuedAt(timestamp);
                }}
                className="p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
            />

            <textarea
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
            />

            <input
                type="url"
                placeholder="URI (optional)"
                value={uri}
                onChange={(e) => setUri(e.target.value)}
                className="p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />

            <button
                type="submit"
                className="mt-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2 px-4 rounded-lg shadow-md"
            >
                Submit
            </button>
        </form>
    );
}
