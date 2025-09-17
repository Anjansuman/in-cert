/*
  Warnings:

  - Added the required column `jwt` to the `Certificate` table without a default value. This is not possible if the table is not empty.
  - Added the required column `nftHash` to the `Certificate` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "public"."Certificate" ADD COLUMN     "jwt" TEXT NOT NULL,
ADD COLUMN     "nftHash" TEXT NOT NULL;
