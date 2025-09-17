/*
  Warnings:

  - You are about to drop the column `verified` on the `Institution` table. All the data in the column will be lost.

*/
-- CreateEnum
CREATE TYPE "public"."VerificationStatus" AS ENUM ('NOT_VERIFIED', 'PENDING', 'VERIFIED', 'FORGED');

-- AlterTable
ALTER TABLE "public"."Institution" DROP COLUMN "verified",
ADD COLUMN     "verification" "public"."VerificationStatus" NOT NULL DEFAULT 'NOT_VERIFIED';
