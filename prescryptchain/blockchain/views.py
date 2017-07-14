# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Python libs
import hashlib
# Django packages
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView
# Our Models
from .forms import NewPrescriptionForm
from .models import Prescription, Block



class AddPrescriptionView(View):
    ''' Simple Rx Form '''
    template = 'blockchain/blockchain/new_rx.html'

    def get(self, request, *args, **kwargs):
        template = 'blockchain/new_rx.html'
        form = NewPrescriptionForm
        return render(request, template ,{"form": form,})

    def post(self, request, *args, **kwargs):
        template = 'blockchain/new_rx.html'
        form = NewPrescriptionForm(request.POST)
        if form.is_valid():
            rx = form.save(commit = False)
            rx.save()
            hash_object = hashlib.sha256(str(rx.timestamp))
            rx.signature = hash_object.hexdigest()
            rx.save()

        return redirect('/')


def rx_detail(request, hash_rx=False):
    ''' Get a hash and return the rx '''
    if request.GET.get("hash_rx", False):
        hash_rx = request.GET.get("hash_rx")

    if hash_rx:
        context = {}
        try:
            rx = Prescription.objects.get(signature=hash_rx)
            context["rx"] = rx
            return render(request, "blockchain/rx_detail.html", context)

        except Exception as e:
            return redirect("/block/?block_hash=%s" % hash_rx)

    return redirect("/")


def block_detail(request, block_hash=False):
    ''' Get a hash and return the block '''
    if request.GET.get("block_hash", False):
        block_hash = request.GET.get("block_hash")

    if block_hash:
        context = {}
        try:
            block = Block.objects.get(hash_block=block_hash)
            context["block_object"] = block
            return render(request, "blockchain/block_detail.html", context)

        except Exception as e:
            print("Error found: %s, type: %s" % (e, type(e)))

    return redirect("/")
