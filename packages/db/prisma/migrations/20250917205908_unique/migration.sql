/*
  Warnings:

  - A unique constraint covering the columns `[nftHash]` on the table `Certificate` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[jwt]` on the table `Certificate` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "Certificate_nftHash_key" ON "public"."Certificate"("nftHash");

-- CreateIndex
CREATE UNIQUE INDEX "Certificate_jwt_key" ON "public"."Certificate"("jwt");
